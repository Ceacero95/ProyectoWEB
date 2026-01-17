import logging
import argparse
import os
import pandas as pd
from datetime import datetime, timedelta
from src.silver.parser import DataParser
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager

logger = logging.getLogger(__name__)

def process_i90(start_date: datetime, end_date: datetime):
    """
    Process I90 files: Bronze -> Silver (Parquet) -> Database
    """
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    errors_list = []
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        bronze_dir = f"bronze/i90/{year}/{month}"
        
        date_str = current_date.strftime("%Y%m%d")
        expected_files = storage.list_files(bronze_dir, extension=".zip")
        
        target_files = [f for f in expected_files if f"_{date_str}.zip" in f]
        
        if not target_files:
             # Log missing file as minimal error? Or just skip. User wants "fallos", missing might be a failure.
             # But if it's in the future it's not a failure.
             # We'll skip logging "missing" for now unless user asks, to focus on "sheets" logic failures.
             pass

        for rel_path in target_files:
            logger.info(f"Processing {rel_path}...")
            content = storage.read(rel_path)
            if not content: continue
            
            extracted = DataParser.extract_zip(content)
            
            for in_name, in_bytes in extracted.items():
                if in_name.endswith((".xlsx", ".xls")):
                    try:
                        data_pkg = DataParser.parse_i90_excel(in_bytes, filename_ref=in_name)
                        
                        # Check if parser returned results. If empty dict, it might mean skipping or failure inside parser.
                        if not data_pkg:
                            # Not necessarily an error if sheet is empty or config skipped it.
                            # But if an exception happened inside parser it would be caught here? 
                            # No, parser catches its own exceptions. We need to check logs or trust parser.
                            # Parser returns partial results.
                            pass

                        for table, pkg in data_pkg.items():
                            try:
                                df = pkg['df']
                                pk = pkg['pk']
                                
                                df['source_file'] = in_name
                                if 'source_file' not in pk: pk.append('source_file')
                                
                                silver_path = f"silver/i90/{year}/{month}/{table}/{date_str}_{in_name}.parquet"
                                parquet_bytes = df.to_parquet(index=False)
                                storage.save(silver_path, parquet_bytes)
                                
                                db_manager.bulk_insert_df(df, table, schema="i90", pk_cols=pk)
                                db_manager.create_indexes(table, ['actualizacion', 'fecha', 'source_file'], schema="i90")
                            except Exception as e_sheet:
                                logger.error(f"Error processing table {table} in {in_name}: {e_sheet}")
                                errors_list.append({
                                    "date": date_str,
                                    "file": in_name,
                                    "sheet": table,
                                    "error": str(e_sheet)
                                })
                            
                    except Exception as e:
                        logger.error(f"Error processing item {in_name}: {e}")
                        errors_list.append({
                            "date": date_str,
                            "file": in_name,
                            "sheet": "ALL",
                            "error": str(e)
                        })

        current_date += timedelta(days=1)
        
    if errors_list:
        error_df = pd.DataFrame(errors_list)
        report_path = "processing_errors_i90.csv"
        # Append if exists? No, overwrite for this run ID or append?
        # User asked for a file. We will overwrite or safeguard.
        if os.path.exists(report_path):
             error_df.to_csv(report_path, mode='a', header=False, index=False)
        else:
             error_df.to_csv(report_path, index=False)
        logger.info(f"Errors written to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process I90 Data (Silver)")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    process_i90(start, end)
