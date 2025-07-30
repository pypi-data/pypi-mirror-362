import os
import pytest
from click.testing import CliRunner
from cli.item_cli import cli
from alembic.config import Config
from alembic import command

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    test_db_path = tmp_path / "cli_test_disable_enable.db"
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{test_db_path}")
    command.upgrade(alembic_cfg, "head")
    monkeypatch.setenv("DAO_TEST_DB", str(test_db_path))
    yield

def test_disable_enable_and_list_disabled():
    runner = CliRunner()
    # Add three items
    runner.invoke(cli, ['add'], input='Active1\nDesc1\ntag1\n1\nTrue\n')
    runner.invoke(cli, ['add'], input='Active2\nDesc2\ntag2\n2\nTrue\n')
    runner.invoke(cli, ['add'], input='ToDisable\nDesc3\ntag3\n3\nTrue\n')
    # Disable item 3
    result = runner.invoke(cli, ['disable', '3'])
    assert 'disabled' in result.output
    # List active
    result = runner.invoke(cli, ['list'])
    assert 'ToDisable' not in result.output
    # List disabled
    result = runner.invoke(cli, ['list-disabled'])
    assert 'ToDisable' in result.output
    # Enable item 3
    result = runner.invoke(cli, ['enable', '3'])
    assert 'enabled' in result.output
    # List active again
    result = runner.invoke(cli, ['list'])
    assert 'ToDisable' in result.output

def test_edit_blocked_for_disabled():
    runner = CliRunner()
    runner.invoke(cli, ['add'], input='BlockEdit\nDesc\ntag\n1\nTrue\n')
    runner.invoke(cli, ['disable', '1'])
    result = runner.invoke(cli, ['edit', '1', '--name', 'ShouldFail'])
    assert 'cannot be edited' in result.output

def test_list_details_shows_disabled():
    runner = CliRunner()
    runner.invoke(cli, ['add'], input='WithDetail\nDesc\ntag\n1\nTrue\n')
    # Add details via direct SQL
    import sqlite3
    db_path = os.environ["DAO_TEST_DB"]
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO item_details (item_id, key, value, is_active) VALUES (?, ?, ?, ?)', (1, 'foo', 'bar', 1))
        c.execute('INSERT INTO item_details (item_id, key, value, is_active) VALUES (?, ?, ?, ?)', (1, 'baz', 'qux', 1))
        conn.commit()
    # Disable item (cascades to details)
    runner.invoke(cli, ['disable', '1'])
    result = runner.invoke(cli, ['list-details', '1'])
    assert 'Yes' in result.output  # Disabled column
    assert 'foo' in result.output and 'baz' in result.output
    # Enable item (cascades to details)
    runner.invoke(cli, ['enable', '1'])
    result = runner.invoke(cli, ['list-details', '1'])
    assert 'No' in result.output
