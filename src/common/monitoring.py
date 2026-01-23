import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from src.common.database import DatabaseManager, get_engine

logger = logging.getLogger(__name__)

class MonitoringManager:
    """
    Manages the Control ETL Status table to track data gaps and freshness.
    """
    
    TABLE_NAME = "control_etl_status"
    SCHEMA = "public"

    def __init__(self):
        self.db_manager = DatabaseManager()
        self._ensure_control_table()

    def _ensure_control_table(self):
        """
        Creates the control table if it doesn't exist.
        """
        ddl = f"""
        CREATE TABLE IF NOT EXISTS {self.SCHEMA}.{self.TABLE_NAME} (
            table_name VARCHAR(100) PRIMARY KEY,
            last_data_date DATE,
            last_checked_at TIMESTAMP,
            missing_days_count INTEGER,
            missing_days_list TEXT,
            status VARCHAR(20)
        );
        """
        try:
            engine = get_engine()
            with engine.begin() as conn:
                conn.execute(text(ddl))
        except Exception as e:
            logger.error(f"Error creating control table: {e}")

    def update_control_table(self, target_table: str, target_schema: str, start_date_str: str = '2025-01-01'):
        """
        Checks the target table for gaps since start_date and updates the control table.
        """
        try:
            engine = get_engine()
            full_target = f"{target_schema}.{target_table}"
            
            # 1. Get max date and all distinct dates
            with engine.connect() as conn:
                # Check existence
                exists = conn.execute(
                    text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = :s AND table_name = :t)"),
                    {"s": target_schema, "t": target_table}
                ).scalar()
                
                if not exists:
                    logger.warning(f"Target table {full_target} does not exist.")
                    return

                # Get Max Date
                max_date = conn.execute(text(f"SELECT MAX(fecha) FROM {full_target}")).scalar()
                
                # Get Distinct Dates
                query_dist = text(f"SELECT DISTINCT fecha FROM {full_target} WHERE fecha >= :start")
                existing_dates = {r[0] for r in conn.execute(query_dist, {"start": start_date_str}).fetchall()}
            
            # 2. Calculate Gaps
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            # We usually expect data up to Yesterday.
            # But let's check up to Today or Max Date.
            # If max_date is None, empty table.
            
            if max_date is None:
                missing_count = -1
                missing_list = "EMPTY TABLE"
                status = "EMPTY"
            else:
                # Range from start_date to min(today, max_date + 1??)
                # Actually we want to know gaps up to TODAY (or yesterday).
                # If we assume daily data, we check up to yesterday.
                # Let's check up to yesterday.
                check_end_date = today - pd.Timedelta(days=1)
                
                if check_end_date < start_date:
                    expected_dates = []
                else:
                    expected_dates = pd.date_range(start=start_date, end=check_end_date).date
                
                missing_dates = sorted([d for d in expected_dates if d not in existing_dates])
                
                missing_count = len(missing_dates)
                if missing_count > 0:
                    # Truncate list if too long
                    missing_str_list = [d.strftime('%Y-%m-%d') for d in missing_dates]
                    if len(missing_str_list) > 20:
                        missing_list = ",".join(missing_str_list[:20]) + ",..."
                    else:
                        missing_list = ",".join(missing_str_list)
                    status = "GAPS"
                else:
                    missing_list = ""
                    status = "OK"
                
                # Check if STALE (last data is old)
                if max_date < check_end_date:
                    status = "STALE" if status == "OK" else "GAPS/STALE"

            # 3. Upsert into Control Table
            upsert_sql = text(f"""
                INSERT INTO {self.SCHEMA}.{self.TABLE_NAME} 
                (table_name, last_data_date, last_checked_at, missing_days_count, missing_days_list, status)
                VALUES (:name, :last_date, :now, :cnt, :list, :status)
                ON CONFLICT (table_name) DO UPDATE SET
                last_data_date = EXCLUDED.last_data_date,
                last_checked_at = EXCLUDED.last_checked_at,
                missing_days_count = EXCLUDED.missing_days_count,
                missing_days_list = EXCLUDED.missing_days_list,
                status = EXCLUDED.status
            """)
            
            with engine.begin() as conn:
                conn.execute(upsert_sql, {
                    "name": target_table,
                    "last_date": max_date,
                    "now": datetime.now(),
                    "cnt": missing_count,
                    "list": missing_list,
                    "status": status
                })
                
            logger.info(f"Updated control status for {target_table}: {status}")

        except Exception as e:
            logger.error(f"Error updating control table for {target_table}: {e}")
