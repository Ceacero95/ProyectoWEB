import logging
import argparse
import pandas as pd
from datetime import datetime, timedelta
from src.silver.parser import DataParser
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager

logger = logging.getLogger(__name__)

def process_i3(start_date: datetime, end_date: datetime):
    """
    Process I3 files: Bronze -> Silver (Parquet) -> Database
    Reuse I90 logic mostly but specific to I3 structure if needed.
    """
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        bronze_dir = f"bronze/i3/{year}/{month}"
        
        date_str = current_date.strftime("%Y%m%d")
        expected_files = storage.list_files(bronze_dir, extension=".zip")
        # Filter for I3 specific archives if multiple exist? Usually esios_{id}_...
        target_files = [f for f in expected_files if f"_{date_str}.zip" in f]
        
        for rel_path in target_files:
            logger.info(f"Processing {rel_path}...")
            content = storage.read(rel_path)
            if not content: continue
            
            extracted = DataParser.extract_zip(content)
            
            for in_name, in_bytes in extracted.items():
                if in_name.endswith((".xlsx", ".xls")):
                    try:
                        # Use same parser as I90 for now as structure is similar PDBF
                        data_pkg = DataParser.parse_i90_excel(in_bytes, filename_ref=in_name)
                        
                        for table, pkg in data_pkg.items():
                            df = pkg['df']
                            pk = pkg['pk']
                            
                            df['source_file'] = in_name
                            if 'source_file' not in pk: pk.append('source_file')
                            
                            silver_path = f"silver/i3/{year}/{month}/{table}/{date_str}_{in_name}.parquet"
                            storage.save(silver_path, df.to_parquet(index=False))
                            
                            if pk:
                                df.drop_duplicates(subset=pk, keep='first', inplace=True)
                            
                            # Use i3 schema
                            db_manager.bulk_insert_df(df, table, schema="i3", pk_cols=pk)
                            db_manager.create_indexes(table, ['actualizacion', 'fecha', 'source_file'], schema="i3")
                            
                    except Exception as e:
                        logger.error(f"Error processing I3 item {in_name}: {e}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process I3 Data (Silver)")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    process_i3(start, end)
