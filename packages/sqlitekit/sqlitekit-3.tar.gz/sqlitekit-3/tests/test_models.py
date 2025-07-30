import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database.models import Category, Item, ItemDetail
import pendulum
from alembic.config import Config
from alembic import command

def run_migrations(db_path):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

def test_database_schema_exists(tmp_path):
    test_db = tmp_path / "test_models.db"
    run_migrations(test_db)
    engine = create_engine(f"sqlite:///{test_db}")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'categories' in tables
    assert 'items' in tables
    assert 'item_details' in tables

def test_category_item_detail_crud(tmp_path):
    test_db = tmp_path / "test_models.db"
    run_migrations(test_db)
    engine = create_engine(f"sqlite:///{test_db}")
    Session = sessionmaker(bind=engine)
    session = Session()
    cat = Category(name="cat1")
    session.add(cat)
    session.commit()
    item = Item(name="item1", description="desc", created_at=pendulum.now('UTC'), updated_at=pendulum.now('UTC'), is_active=True, tags="t1", category_id=cat.id)
    session.add(item)
    session.commit()
    detail = ItemDetail(item_id=item.id, key="k1", value="v1")
    session.add(detail)
    session.commit()
    cat_db = session.query(Category).first()
    item_db = session.query(Item).first()
    detail_db = session.query(ItemDetail).first()
    assert cat_db.name == "cat1"
    assert item_db.name == "item1"
    assert item_db.category_id == cat_db.id
    assert detail_db.item_id == item_db.id
    assert detail_db.key == "k1"
    assert detail_db.value == "v1"
    session.close()
