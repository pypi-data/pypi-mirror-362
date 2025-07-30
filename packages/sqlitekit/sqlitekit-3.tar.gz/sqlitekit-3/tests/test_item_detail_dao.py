import pytest
from dao.item_detail_dao import ItemDetailDAO
from alembic.config import Config
from alembic import command
import os

def run_migrations(db_path):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = tmp_path / "dao_test_item_details.db"
    run_migrations(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["DAO_TEST_DB"]

def test_add_and_get_detail():
    dao = ItemDetailDAO()
    detail = dao.add_detail(1, 'color', 'red')
    got = dao.get_detail(detail.id)
    assert got is not None
    assert got.key == 'color'
    assert got.value == 'red'

def test_list_edit_delete_detail():
    dao = ItemDetailDAO()
    d1 = dao.add_detail(1, 'color', 'red')
    d2 = dao.add_detail(1, 'size', 'large')
    details = dao.list_details(item_id=1)
    assert any(d.id == d1.id for d in details)
    updated = dao.edit_detail(d1.id, key='shade', value='blue')
    assert updated
    got = dao.get_detail(d1.id)
    assert got.key == 'shade'
    assert got.value == 'blue'
    deleted = dao.delete_detail(d1.id)
    assert deleted
    assert dao.get_detail(d1.id) is None
