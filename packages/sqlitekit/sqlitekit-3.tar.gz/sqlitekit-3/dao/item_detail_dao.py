from database.models import ItemDetail
from typing import List, Optional
import sqlite3
import os
import pendulum

class ItemDetailDAO:
    def add_detail(self, item_id: int, key: str, value: str, is_active: bool = True) -> ItemDetail:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO item_details (item_id, key, value, is_active) VALUES (?, ?, ?, ?)''',
                      (item_id, key, value, int(is_active)))
            conn.commit()
            detail_id = c.lastrowid
            return ItemDetail(id=detail_id, item_id=item_id, key=key, value=value, is_active=is_active)

    def disable_detail(self, detail_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE item_details SET is_active = 0 WHERE id = ?', (detail_id,))
            conn.commit()
            return c.rowcount > 0

    def enable_detail(self, detail_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE item_details SET is_active = 1 WHERE id = ?', (detail_id,))
            conn.commit()
            return c.rowcount > 0

    def list_disabled_details(self, item_id: int = None) -> list:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            if item_id is not None:
                c.execute('SELECT * FROM item_details WHERE item_id = ? AND is_active = 0', (item_id,))
            else:
                c.execute('SELECT * FROM item_details WHERE is_active = 0')
            columns = [desc[0] for desc in c.description]
            return [ItemDetail(**dict(zip(columns, row))) for row in c.fetchall()]

    def get_detail(self, detail_id: int) -> Optional[ItemDetail]:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM item_details WHERE id = ?', (detail_id,))
            row = c.fetchone()
            if row:
                columns = [desc[0] for desc in c.description]
                data = dict(zip(columns, row))
                return ItemDetail(**data)
            return None

    def list_details(self, item_id: int = None) -> List[ItemDetail]:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            if item_id is not None:
                c.execute('SELECT * FROM item_details WHERE item_id = ?', (item_id,))
            else:
                c.execute('SELECT * FROM item_details')
            columns = [desc[0] for desc in c.description]
            return [ItemDetail(**dict(zip(columns, row))) for row in c.fetchall()]

    def edit_detail(self, detail_id: int, key: str = None, value: str = None) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM item_details WHERE id = ?', (detail_id,))
            if not c.fetchone():
                return False
            fields = []
            values = []
            if key is not None:
                fields.append('key = ?')
                values.append(key)
            if value is not None:
                fields.append('value = ?')
                values.append(value)
            if not fields:
                return False
            values.append(detail_id)
            q = f"UPDATE item_details SET {', '.join(fields)} WHERE id = ?"
            c.execute(q, values)
            conn.commit()
            return True

    def delete_detail(self, detail_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM item_details WHERE id = ?', (detail_id,))
            conn.commit()
            return c.rowcount > 0
