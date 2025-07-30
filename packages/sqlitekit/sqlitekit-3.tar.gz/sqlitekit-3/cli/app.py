from cli.item_cli import cli as item_cli
from cli.item_detail_cli import item_detail
from cli.db_cli import db_init
from cli.bash_cli import bash
from cli.db_manage_cli import db_manage

import click

@click.group()
@click.version_option(package_name="sqlitekit")
def cli():
    pass

from shared.db_path_config import load_db_path
from shared.db_check import db_and_tables_exist

REQUIRED_TABLES = ["items", "item_details"]

db_path = load_db_path()
db_ready = db_and_tables_exist(db_path, REQUIRED_TABLES)

if db_ready:
    cli.add_command(item_cli, name="item")
    cli.add_command(item_detail, name="item-detail")
    cli.add_command(bash)
    cli.add_command(db_manage, name="db")
else:
    cli.add_command(db_init)

if __name__ == "__main__":
    cli()
