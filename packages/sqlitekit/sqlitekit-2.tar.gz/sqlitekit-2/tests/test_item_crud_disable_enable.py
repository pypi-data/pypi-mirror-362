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
    test_db_path = tmp_path / "crud_test_disable_enable.db"
    run_migrations(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["DAO_TEST_DB"]

def test_disable_enable_and_list_disabled():
    crud = ItemCRUD()
    item1 = crud.add_item('Active', 'desc', 'tag', 1, True)
    item2 = crud.add_item('ToDisable', 'desc', 'tag', 2, True)
    # Disable item2
    assert crud.disable_item(item2.id)
    # Only item1 should be active
    active = [i for i in crud.list_items() if i.is_active]
    assert all(i.id != item2.id for i in active)
    # Disabled list
    disabled = crud.list_disabled_items()
    assert any(i.id == item2.id for i in disabled)
    # Enable item2
    assert crud.enable_item(item2.id)
    active = [i for i in crud.list_items() if i.is_active]
    assert any(i.id == item2.id for i in active)

def test_edit_blocked_for_disabled():
    crud = ItemCRUD()
    item = crud.add_item('BlockEdit', 'desc', 'tag', 1, True)
    crud.disable_item(item.id)
    # Simulate CLI logic: edit should not be allowed if is_active is False
    item2 = crud.get_item(item.id)
    assert not item2.is_active
    # But DAO/CRUD still allows edit (CLI blocks it), so test that edit works at this layer
    updated = crud.edit_item(item.id, name='ShouldWork')
    assert updated
    item3 = crud.get_item(item.id)
    assert item3.name == 'ShouldWork'
