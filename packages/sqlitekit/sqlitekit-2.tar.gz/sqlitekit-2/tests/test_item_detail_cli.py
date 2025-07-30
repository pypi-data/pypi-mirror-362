import os
import pytest
from click.testing import CliRunner
from cli.item_detail_cli import item_detail
from alembic.config import Config
from alembic import command

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    test_db_path = tmp_path / "cli_test_item_details.db"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{test_db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DAO_TEST_DB", str(test_db_path))
    yield

def test_add_and_list_cli():
    runner = CliRunner()
    # Add detail
    result = runner.invoke(item_detail, ['add'], input='1\ncolor\nred\n')
    assert 'Item detail added' in result.output
    # List details
    result = runner.invoke(item_detail, ['list', '--item-id', '1'])
    assert 'color' in result.output and 'red' in result.output

def test_edit_and_delete_cli():
    runner = CliRunner()
    runner.invoke(item_detail, ['add'], input='1\nsize\nlarge\n')
    # Edit
    result = runner.invoke(item_detail, ['edit', '1', '--key', 'length', '--value', 'long'])
    assert 'Item detail updated' in result.output
    # List and check
    result = runner.invoke(item_detail, ['list', '--item-id', '1'])
    assert 'length' in result.output and 'long' in result.output
    # Delete
    result = runner.invoke(item_detail, ['delete', '1'])
    assert 'Item detail deleted' in result.output
    # List again
    result = runner.invoke(item_detail, ['list', '--item-id', '1'])
    assert 'No item details found' in result.output
