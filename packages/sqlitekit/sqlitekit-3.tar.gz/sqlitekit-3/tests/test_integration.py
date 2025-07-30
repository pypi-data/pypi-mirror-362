import os
import pytest
from click.testing import CliRunner
from app import cli
from alembic.config import Config
from alembic import command

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    test_db_path = tmp_path / "integration_test_items.db"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{test_db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DAO_TEST_DB", str(test_db_path))
    yield

def test_full_crud_integration():
    runner = CliRunner()
    # Add item
    result = runner.invoke(cli, ['add'], input='IntegrationItem\nIntegrationDesc\ntagX\n1\nTrue\n')
    assert 'Item added' in result.output
    # List
    result = runner.invoke(cli, ['list'])
    assert 'IntegrationItem' in result.output
    # Edit
    result = runner.invoke(cli, ['edit', '1', '--name', 'IntegrationRenamed'])
    assert 'Item updated' in result.output
    # List again
    result = runner.invoke(cli, ['list'])
    assert 'IntegrationRenamed' in result.output
    # Delete
    result = runner.invoke(cli, ['delete', '1'])
    assert 'Item deleted' in result.output
    # List final
    result = runner.invoke(cli, ['list'])
    assert 'No items found' in result.output
