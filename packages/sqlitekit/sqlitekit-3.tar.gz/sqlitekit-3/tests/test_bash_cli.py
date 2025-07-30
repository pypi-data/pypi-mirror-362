import subprocess
import sqlite3
from pathlib import Path
import pytest
import os


@pytest.fixture(autouse=True)
def clean_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_items.db"
    alembic_cfg = None
    try:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        raise RuntimeError("Alembic migration failed") from e
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("DAO_TEST_DB", str(db_path))
    yield

def count_items(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM items')
    count = cur.fetchone()[0]
    conn.close()
    return count

def count_item_details(db_path, item_id=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if item_id is not None:
        cur.execute('SELECT COUNT(*) FROM item_details WHERE item_id=?', (item_id,))
    else:
        cur.execute('SELECT COUNT(*) FROM item_details')
    count = cur.fetchone()[0]
    conn.close()
    return count

def test_bash_cli_run_items(tmp_path):
    db_path = tmp_path / "test_items.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["DAO_TEST_DB"] = str(db_path)
    # Add 3 items using the bash CLI
    result = subprocess.run(['python', 'app.py', 'bash', 'faker', 'run-items', '3'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert 'Item added:' in result.stdout
    assert count_items(db_path) == 3

def test_bash_cli_run_item_details(tmp_path):
    db_path = tmp_path / "test_items.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["DAO_TEST_DB"] = str(db_path)
    # Add 1 item first
    subprocess.run(['python', 'app.py', 'bash', 'faker', 'run-items', '1'], capture_output=True, text=True, env=env)
    # Add 2 details to item_id=1
    result = subprocess.run(['python', 'app.py', 'bash', 'faker', 'run-item-details', '2', '1'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert 'Item detail added:' in result.stdout
    assert count_item_details(db_path, 1) == 2
