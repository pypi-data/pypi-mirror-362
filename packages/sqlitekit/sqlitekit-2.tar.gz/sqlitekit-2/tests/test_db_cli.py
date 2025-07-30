import subprocess
import os
import sqlite3
from pathlib import Path
import pytest


def test_db_init_command_creates_schema(tmp_path):
    db_path = tmp_path / "test_items.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    result = subprocess.run(['python', 'app.py', 'db-init'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert 'Database schema initialized' in result.stdout
    assert db_path.exists()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = {row[0] for row in cur.fetchall()}
    conn.close()
    assert 'items' in tables
    assert 'item_details' in tables
    assert 'categories' in tables
