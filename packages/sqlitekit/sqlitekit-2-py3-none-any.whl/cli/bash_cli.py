import click
import subprocess
import os
from pathlib import Path

BASH_SCRIPTS_DIR = Path(__file__).parent.parent / 'etl'
FAKE_ITEMS_SCRIPT = BASH_SCRIPTS_DIR / 'fake_items.sh'
FAKE_ITEM_DETAILS_SCRIPT = BASH_SCRIPTS_DIR / 'fake_item_details.sh'

def run_bash_script(script_path, args):
    env = os.environ.copy()
    db_path = env.get('DB_PATH')
    # Always pass DB_PATH to subprocess for test/production isolation
    if db_path:
        env['DB_PATH'] = db_path
    result = subprocess.run(['bash', str(script_path)] + list(args), capture_output=True, text=True, env=env)
    click.echo(result.stdout)
    if result.returncode != 0:
        click.echo(result.stderr, err=True)
        raise click.ClickException(f"Script failed: {script_path}")

@click.group()
def bash():
    """Run bash scripts for data generation and utilities."""
    pass

@bash.group()
def faker():
    """Run faker-related bash scripts."""
    pass

@faker.command('run-items')
@click.argument('num_items', type=int)
def run_items(num_items):
    """Run the fake_items.sh script to add NUM_ITEMS fake items."""
    run_bash_script(FAKE_ITEMS_SCRIPT, [str(num_items)])

@faker.command('run-item-details')
@click.argument('num_details', type=int)
@click.argument('item_id', type=int)
def run_item_details(num_details, item_id):
    """Run the fake_item_details.sh script to add NUM_DETAILS to ITEM_ID."""
    run_bash_script(FAKE_ITEM_DETAILS_SCRIPT, [str(num_details), str(item_id)])
