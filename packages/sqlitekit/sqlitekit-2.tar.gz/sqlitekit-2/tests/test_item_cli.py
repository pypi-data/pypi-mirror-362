import os
import pytest
from click.testing import CliRunner
from cli.item_cli import cli
from alembic.config import Config
from alembic import command

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    test_db_path = tmp_path / "cli_test_items.db"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{test_db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DAO_TEST_DB", str(test_db_path))
    yield

def test_add_and_list_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['add'], input='Item1\nDesc1\ntag1\n1\nTrue\n')
    assert 'Item added' in result.output
    result = runner.invoke(cli, ['list'])
    assert 'Item1' in result.output

def test_edit_and_delete_cli():
    runner = CliRunner()
    runner.invoke(cli, ['add'], input='Item2\nDesc2\ntag2\n1\nTrue\n')
    result = runner.invoke(cli, ['edit', '1', '--name', 'Renamed'])
    assert 'Item updated' in result.output
    result = runner.invoke(cli, ['delete', '1'])
    assert 'Item deleted' in result.output
    result = runner.invoke(cli, ['list'])
    assert 'No items found' in result.output
