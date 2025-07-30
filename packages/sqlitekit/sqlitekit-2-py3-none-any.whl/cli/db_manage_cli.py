import click
import os
import sqlite3
from shared.db_path_config import load_db_path

@click.group()
def db_manage():
    """Database management commands."""
    pass

@db_manage.command('dir')
def db_dir():
    """Display the directory and path of the database file."""
    db_path = load_db_path()
    click.echo(f"Database path: {db_path}")
    click.echo(f"Database directory: {os.path.dirname(db_path)}")

@db_manage.command('wipe')
def db_wipe():
    """Delete all data from all tables in the database, but keep the schema."""
    db_path = load_db_path()
    if not os.path.exists(db_path):
        click.echo("Database file does not exist.")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
    conn.commit()
    conn.close()
    click.echo("All data wiped from all tables.")

@db_manage.command('delete')
def db_delete():
    """Delete the database file from disk."""
    db_path = load_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)
        click.echo(f"Database file deleted: {db_path}")
    else:
        click.echo("Database file does not exist.")
