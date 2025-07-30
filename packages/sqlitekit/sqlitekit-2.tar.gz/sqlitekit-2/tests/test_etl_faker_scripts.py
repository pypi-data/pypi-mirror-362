import subprocess
import sqlite3
import os
import pytest
from pathlib import Path

ITEMS_SCRIPT = Path('etl/fake_items.sh')
DETAILS_SCRIPT = Path('etl/fake_item_details.sh')

@pytest.fixture(scope='function')
def clean_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_items.db"
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("DAO_TEST_DB", str(db_path))
    yield

@pytest.mark.usefixtures('clean_db')
def test_fake_items_script_adds_items(tmp_path):
    db_path = tmp_path / "test_items.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["DAO_TEST_DB"] = str(db_path)
    result = subprocess.run(['bash', str(ITEMS_SCRIPT), '2'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    # Check DB for 2 items
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM items')
    count = cur.fetchone()[0]
    conn.close()
    assert count == 2

@pytest.mark.usefixtures('clean_db')
def test_fake_item_details_script_adds_details(tmp_path):
    db_path = tmp_path / "test_items.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["DAO_TEST_DB"] = str(db_path)
    subprocess.run(['bash', str(ITEMS_SCRIPT), '1'], capture_output=True, text=True, env=env)
    result = subprocess.run(['bash', str(DETAILS_SCRIPT), '3', '1'], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    # Check DB for 3 item details
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM item_details WHERE item_id = 1')
    count = cur.fetchone()[0]
    conn.close()
    assert count == 3
