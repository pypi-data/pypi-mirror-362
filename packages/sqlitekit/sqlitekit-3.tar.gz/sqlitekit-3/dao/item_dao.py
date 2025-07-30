from database.models import Item
from typing import List, Optional
import sqlite3
import os
import pendulum

class ItemDAO:
    def add_item(self, name, description, tags, category_id, is_active=True) -> Item:
        now = pendulum.now('UTC').isoformat()
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO items (name, description, created_at, updated_at, is_active, tags, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (name, description, now, now, int(is_active), tags, category_id))
            conn.commit()
            item_id = c.lastrowid
            return Item(id=item_id, name=name, description=description, created_at=now, updated_at=now, is_active=is_active, tags=tags, category_id=category_id)

    def disable_item(self, item_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE items SET is_active = 0, updated_at = ? WHERE id = ?', (pendulum.now('UTC').isoformat(), item_id))
            c.execute('UPDATE item_details SET is_active = 0 WHERE item_id = ?', (item_id,))
            conn.commit()
            return c.rowcount > 0

    def enable_item(self, item_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE items SET is_active = 1, updated_at = ? WHERE id = ?', (pendulum.now('UTC').isoformat(), item_id))
            c.execute('UPDATE item_details SET is_active = 1 WHERE item_id = ?', (item_id,))
            conn.commit()
            return c.rowcount > 0

    def list_disabled_items(self) -> list:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM items WHERE is_active = 0')
            columns = [desc[0] for desc in c.description]
            return [Item(**dict(zip(columns, row))) for row in c.fetchall()]

    def get_item(self, item_id: int) -> Optional[Item]:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            row = c.fetchone()
            if row:
                # Map row to Item using column names
                columns = [desc[0] for desc in c.description]
                data = dict(zip(columns, row))
                return Item(**data)
            return None

    def list_items(self) -> List[Item]:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM items')
            columns = [desc[0] for desc in c.description]
            return [Item(**dict(zip(columns, row))) for row in c.fetchall()]

    def edit_item(self, item_id, name=None, description=None, tags=None, category_id=None, is_active=None) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM items WHERE id = ?', (item_id,))
            if not c.fetchone():
                return False
            fields = []
            values = []
            if name is not None:
                fields.append('name = ?')
                values.append(name)
            if description is not None:
                fields.append('description = ?')
                values.append(description)
            if tags is not None:
                fields.append('tags = ?')
                values.append(tags)
            if category_id is not None:
                fields.append('category_id = ?')
                values.append(category_id)
            if is_active is not None:
                fields.append('is_active = ?')
                values.append(int(is_active))
            if not fields:
                return False
            fields.append('updated_at = ?')
            values.append(pendulum.now('UTC').isoformat())
            values.append(item_id)
            q = f"UPDATE items SET {', '.join(fields)} WHERE id = ?"
            c.execute(q, values)
            conn.commit()
            return True

    def delete_item(self, item_id: int) -> bool:
        db_path = os.environ.get("DAO_TEST_DB", "sqlitekit_data/items.db")
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM items WHERE id = ?', (item_id,))
            conn.commit()
            return c.rowcount > 0
