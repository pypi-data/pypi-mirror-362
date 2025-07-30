import click
from dao.item_dao import ItemDAO
from shared.db_path_config import load_db_path
from shared.db_check import db_and_tables_exist

dao = ItemDAO()

REQUIRED_TABLES = ["items", "item_details"]

def ensure_db_ready():
    db_path = load_db_path()
    if not db_and_tables_exist(db_path, REQUIRED_TABLES):
        click.echo("Error: Database or required tables not found. Please run 'sqlitekit db-init' first.")
        raise click.ClickException("Database not initialized.")

@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', prompt='Name', help='Name of the item')
@click.option('--description', prompt='Description', help='Description of the item')
@click.option('--tags', prompt='Tags (comma separated)', default='', help='Tags for the item')
@click.option('--category_id', type=int, default=None, help='Category ID (optional)')
@click.option('--is_active', type=bool, default=True, help='Is the item active?')
def add(name, description, tags, category_id, is_active):
    ensure_db_ready()
    item = dao.add_item(name, description, tags, category_id, is_active)
    click.echo(f'Item added: {item.id}')

@cli.command()
def list():
    ensure_db_ready()
    from crud.item_crud import ItemCRUD
    crud = ItemCRUD()
    items = [i for i in crud.list_items() if i.is_active]
    if items:
        click.echo(f"{'ID':<4} {'Name':<16} {'Active':<7} {'Tags':<18} {'Category':<9} {'Created At':<19} {'Updated At':<19}")
        click.echo('-' * 92)
        for item in items:
            click.echo(f"{item.id:<4} {item.name[:15]:<16} {str(bool(item.is_active)):<7} {str(item.tags)[:17]:<18} {str(item.category_id):<9} {str(item.created_at)[:19]:<19} {str(item.updated_at)[:19]:<19}")
    else:
        click.echo('No items found.')

@cli.command('list-disabled')
def list_disabled():
    ensure_db_ready()
    from crud.item_crud import ItemCRUD
    crud = ItemCRUD()
    items = crud.list_disabled_items()
    if items:
        click.echo(f"{'ID':<4} {'Name':<16} {'Active':<7} {'Tags':<18} {'Category':<9} {'Created At':<19} {'Updated At':<19}")
        click.echo('-' * 92)
        for item in items:
            click.echo(f"{item.id:<4} {item.name[:15]:<16} {str(bool(item.is_active)):<7} {str(item.tags)[:17]:<18} {str(item.category_id):<9} {str(item.created_at)[:19]:<19} {str(item.updated_at)[:19]:<19}")
    else:
        click.echo('No disabled items found.')

@cli.command()
@click.argument('item_id', type=int)
def disable(item_id):
    ensure_db_ready()
    from crud.item_crud import ItemCRUD
    crud = ItemCRUD()
    if not crud.disable_item(item_id):
        click.echo('Item not found or already disabled.')
    else:
        click.echo('Item and its details disabled.')

@cli.command()
@click.argument('item_id', type=int)
def enable(item_id):
    ensure_db_ready()
    from crud.item_crud import ItemCRUD
    crud = ItemCRUD()
    if not crud.enable_item(item_id):
        click.echo('Item not found or already enabled.')
    else:
        click.echo('Item and its details enabled.')

@cli.command()
@click.argument('item_id', type=int)
@click.option('--name', help='New name of the item')
@click.option('--description', help='New description of the item')
@click.option('--tags', help='New tags (comma separated)')
@click.option('--category_id', type=int, help='New category ID')
@click.option('--is_active', type=bool, help='Is the item active?')
def edit(item_id, name, description, tags, category_id, is_active):
    ensure_db_ready()
    from crud.item_crud import ItemCRUD
    crud = ItemCRUD()
    item = crud.get_item(item_id)
    if not item:
        click.echo('Item not found.')
        return
    if not getattr(item, 'is_active', True):
        click.echo('This item is disabled and cannot be edited.')
        return
    result = crud.edit_item(item_id, name, description, tags, category_id, is_active)
    if result:
        click.echo('Item updated.')
    else:
        click.echo('Item not found.')

@cli.command('list-details')
@click.argument('item_id', type=int)
def list_details_for_item(item_id):
    """List all item details for a specified item."""
    ensure_db_ready()
    from crud.item_detail_crud import ItemDetailCRUD
    detail_crud = ItemDetailCRUD()
    details = detail_crud.list_details(item_id)
    if not details:
        click.echo("No item details found for this item.")
    else:
        click.echo(f"{'ID':<4} {'Item ID':<8} {'Key':<16} {'Value':<30} {'Disabled'}")
        click.echo('-' * 75)
        for d in details:
            click.echo(f"{d.id:<4} {d.item_id:<8} {d.key[:15]:<16} {str(d.value)[:29]:<30} {'Yes' if not getattr(d, 'is_active', True) else 'No'}")

@cli.command()
@click.argument('item_id', type=int)
def delete(item_id):
    ensure_db_ready()
    # Delete all item details with this item_id first
    from crud.item_detail_crud import ItemDetailCRUD
    detail_crud = ItemDetailCRUD()
    details = detail_crud.list_details(item_id)
    for d in details:
        detail_crud.delete_detail(d.id)
    result = dao.delete_item(item_id)
    if result:
        click.echo('Item deleted.')
    else:
        click.echo('Item not found.')
