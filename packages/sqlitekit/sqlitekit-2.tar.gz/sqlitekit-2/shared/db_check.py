import os
import sqlite3

def db_and_tables_exist(db_path: str, required_tables=None) -> bool:
    """
    Check if the SQLite database file and required tables exist.
    If required_tables is None, checks for 'items' and 'item_details'.
    """
    if required_tables is None:
        required_tables = ["items", "item_details"]
    if not os.path.exists(db_path):
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for table in required_tables:
            cursor.execute(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if cursor.fetchone() is None:
                conn.close()
                return False
        conn.close()
        return True
    except Exception:
        return False
