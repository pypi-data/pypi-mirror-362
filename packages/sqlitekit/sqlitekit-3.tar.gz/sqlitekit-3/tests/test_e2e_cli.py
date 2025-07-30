import subprocess
import os
import tempfile
import shutil
import sys
import pytest

# Helper to run the CLI as a subprocess and return stdout
def run_cli(args, input_text=None, env=None):
    result = subprocess.run(
        [sys.executable, 'app.py'] + args,
        input=input_text,
        text=True,
        capture_output=True,
        env=env
    )
    return result

def test_e2e_item_crud():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'items.db')
    env = os.environ.copy()
    env['DATABASE_URL'] = f"sqlite:///{db_path}"
    env['DAO_TEST_DB'] = db_path
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

    # Add item
    result = run_cli(['add'], input_text="E2EItem\nE2EDesc\ntag1\n1\nTrue\n", env=env)
    assert "Item added" in result.stdout

    # List items
    result = run_cli(['list'], env=env)
    assert "E2EItem" in result.stdout

    # Edit item
    result = run_cli(['edit', '1', '--name', 'E2EItemRenamed'], env=env)
    assert "Item updated" in result.stdout

    # Delete item
    result = run_cli(['delete', '1'], env=env)
    assert "Item deleted" in result.stdout

    # List again
    result = run_cli(['list'], env=env)
    assert "No items found" in result.stdout

    shutil.rmtree(temp_dir)

def test_e2e_item_detail_crud():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'items.db')
    env = os.environ.copy()
    env['DATABASE_URL'] = f"sqlite:///{db_path}"
    env['DAO_TEST_DB'] = db_path
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(alembic_cfg, "head")

    # Add an item first (required for item detail)
    run_cli(['add'], input_text="E2EItem2\nE2EDesc2\ntag2\n1\nTrue\n", env=env)

    # Add detail
    result = run_cli(['item-detail', 'add'], input_text="1\ncolor\nred\n", env=env)
    assert "Item detail added" in result.stdout

    # List details
    result = run_cli(['item-detail', 'list', '--item-id', '1'], env=env)
    assert "color" in result.stdout and "red" in result.stdout

    # Edit detail
    result = run_cli(['item-detail', 'edit', '1', '--key', 'shade', '--value', 'blue'], env=env)
    assert "Item detail updated" in result.stdout

    # Delete detail
    result = run_cli(['item-detail', 'delete', '1'], env=env)
    assert "Item detail deleted" in result.stdout

    shutil.rmtree(temp_dir)
