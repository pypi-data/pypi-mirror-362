import os
import pytest
from click.testing import CliRunner
from cli.item_cli import cli
from alembic.config import Config
from alembic import command

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    test_db_path = tmp_path / "cli_test_items.db"
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{test_db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DAO_TEST_DB", str(test_db_path))
    yield

def test_list_details_for_item():
    runner = CliRunner()
    # Add an item
    result = runner.invoke(cli, ['add'], input='ItemA\nDescA\ntagA\n1\nTrue\n')
    assert 'Item added' in result.output
    # Add details via direct SQL (simulate item_detail_crud)
    import sqlite3
    db_path = os.environ["DAO_TEST_DB"]
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO item_details (item_id, key, value) VALUES (?, ?, ?)', (1, 'foo', 'bar'))
        c.execute('INSERT INTO item_details (item_id, key, value) VALUES (?, ?, ?)', (1, 'baz', 'qux'))
        conn.commit()
    # List details for item 1
    result = runner.invoke(cli, ['list-details', '1'])
    assert 'foo' in result.output
    assert 'baz' in result.output
    assert 'bar' in result.output
    assert 'qux' in result.output
    # List details for non-existent item
    result = runner.invoke(cli, ['list-details', '99'])
    assert 'No item details found' in result.output
