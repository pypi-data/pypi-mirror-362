import pytest
from crud.item_detail_crud import ItemDetailCRUD
from alembic.config import Config
from alembic import command
import os

def run_migrations(db_path):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = tmp_path / "crud_test_item_detail_disable_enable.db"
    run_migrations(test_db_path)
    os.environ["DAO_TEST_DB"] = str(test_db_path)
    yield
    del os.environ["DAO_TEST_DB"]

def test_disable_enable_and_list_disabled():
    crud = ItemDetailCRUD()
    d1 = crud.add_detail(1, 'foo', 'bar', True)
    d2 = crud.add_detail(1, 'baz', 'qux', True)
    # Disable d2
    assert crud.disable_detail(d2.id)
    # Only d1 should be active
    active = [d for d in crud.list_details(1) if d.is_active]
    assert all(d.id != d2.id for d in active)
    # Disabled list
    disabled = crud.list_disabled_details(1)
    assert any(d.id == d2.id for d in disabled)
    # Enable d2
    assert crud.enable_detail(d2.id)
    active = [d for d in crud.list_details(1) if d.is_active]
    assert any(d.id == d2.id for d in active)

def test_disable_enable_detail_does_not_affect_others():
    crud = ItemDetailCRUD()
    d1 = crud.add_detail(1, 'foo', 'bar', True)
    d2 = crud.add_detail(1, 'baz', 'qux', True)
    crud.disable_detail(d1.id)
    # d2 should remain active
    d2_fresh = crud.get_detail(d2.id)
    assert d2_fresh.is_active
    # d1 should be disabled
    d1_fresh = crud.get_detail(d1.id)
    assert not d1_fresh.is_active
