import click

@click.command('db-init')
def db_init():
    """Initialize the database schema using Alembic migrations."""
    import subprocess
    import os
    import sys
    import click
    from shared.db_path_config import load_db_path, save_db_path, DEFAULT_DB_PATH

    env = os.environ.copy()
    db_path = env.get("DB_PATH") or load_db_path()

    if not os.path.exists(db_path):
        import os
        data_dir = os.path.join(os.getcwd(), "sqlitekit_data")
        os.makedirs(data_dir, exist_ok=True)
        cwd_default = os.path.join(data_dir, "items.db")
        click.echo("No database file configured.")
        db_path = click.prompt(
            "Enter the path for your SQLite database",
            default=cwd_default,
            show_default=True
        )
        save_db_path(db_path)
        click.echo(f"Database will be created at: {db_path}")

    # Ensure parent directory exists before running Alembic
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    env["DB_PATH"] = db_path
    db_url = env.get("DATABASE_URL") or db_path
    if not db_url.startswith("sqlite:///"):
        db_url = f"sqlite:///{db_url}"
    env["DATABASE_URL"] = db_url
    result = subprocess.run(['alembic', 'upgrade', 'head'], capture_output=True, text=True, env=env)
    if result.returncode == 0:
        click.echo("Database schema initialized via Alembic.")
    else:
        click.echo(result.stderr, err=True)
        raise click.ClickException("Alembic migration failed.")
