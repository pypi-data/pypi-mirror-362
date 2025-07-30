import pytest
from dao.item_dao import ItemDAO
from alembic.config import Config
from alembic import command
import os

def run_migrations(db_path):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = tmp_path / "dao_test_disable_enable.db"
    run_migrations(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["DAO_TEST_DB"]

def test_disable_enable_and_list_disabled():
    dao = ItemDAO()
    item1 = dao.add_item('Active', 'desc', 'tag', 1, True)
    item2 = dao.add_item('ToDisable', 'desc', 'tag', 2, True)
    # Disable item2
    assert dao.disable_item(item2.id)
    # Only item1 should be active
    active = [i for i in dao.list_items() if i.is_active]
    assert all(i.id != item2.id for i in active)
    # Disabled list
    disabled = dao.list_disabled_items()
    assert any(i.id == item2.id for i in disabled)
    # Enable item2
    assert dao.enable_item(item2.id)
    active = [i for i in dao.list_items() if i.is_active]
    assert any(i.id == item2.id for i in active)

def test_disable_cascades_to_details():
    dao = ItemDAO()
    item = dao.add_item('Cascade', 'desc', 'tag', 1, True)
    import sqlite3
    db_path = os.environ["DAO_TEST_DB"]
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO item_details (item_id, key, value, is_active) VALUES (?, ?, ?, ?)', (item.id, 'foo', 'bar', 1))
        c.execute('INSERT INTO item_details (item_id, key, value, is_active) VALUES (?, ?, ?, ?)', (item.id, 'baz', 'qux', 1))
        conn.commit()
    dao.disable_item(item.id)
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('SELECT is_active FROM item_details WHERE item_id = ?', (item.id,))
        states = [row[0] for row in c.fetchall()]
        assert all(state == 0 for state in states)
    dao.enable_item(item.id)
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('SELECT is_active FROM item_details WHERE item_id = ?', (item.id,))
        states = [row[0] for row in c.fetchall()]
        assert all(state == 1 for state in states)
