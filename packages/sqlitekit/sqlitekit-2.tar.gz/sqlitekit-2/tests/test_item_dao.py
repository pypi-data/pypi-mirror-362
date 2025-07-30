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
    test_db_path = tmp_path / "dao_test_items.db"
    run_migrations(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["DAO_TEST_DB"]

def test_dao_add_and_get():
    dao = ItemDAO()
    item = dao.add_item('A', 'B', 'tags', 1, True)
    got = dao.get_item(item.id)
    assert got is not None
    assert got.name == 'A'

def test_dao_list_and_edit_and_delete():
    dao = ItemDAO()
    item = dao.add_item('A', 'B', 'tags', 1, True)
    items = dao.list_items()
    assert any(i.id == item.id for i in items)
    updated = dao.edit_item(item.id, name='C')
    assert updated
    got = dao.get_item(item.id)
    assert got.name == 'C'
    deleted = dao.delete_item(item.id)
    assert deleted
    assert dao.get_item(item.id) is None
