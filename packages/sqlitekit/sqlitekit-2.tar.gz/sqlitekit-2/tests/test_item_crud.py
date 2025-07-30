import pytest
from crud.item_crud import ItemCRUD
from alembic.config import Config
from alembic import command
import os

def run_migrations(db_path):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = tmp_path / "crud_test_items.db"
    run_migrations(test_db_path)
    os.environ["CRUD_TEST_DB"] = str(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["CRUD_TEST_DB"]
    del os.environ["DAO_TEST_DB"]

def test_item_crud():
    crud = ItemCRUD()
    # Add
    item = crud.add_item('TestName', 'TestDesc', 'tag1,tag2', 1, True)
    assert item.name == 'TestName'
    # List
    items = crud.list_items()
    assert any(i.name == 'TestName' for i in items)
    # Edit
    updated = crud.edit_item(item.id, name='NewName')
    assert updated
    item2 = crud.get_item(item.id)
    assert item2.name == 'NewName'
    # Delete
    deleted = crud.delete_item(item.id)
    assert deleted
    assert not crud.get_item(item.id)
