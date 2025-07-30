import click
from crud.item_detail_crud import ItemDetailCRUD

@click.group()
def item_detail():
    """Manage item details."""
    pass

@item_detail.command()
@click.option('--item-id', prompt=True, type=int, help='Item ID')
@click.option('--key', prompt=True, help='Detail key')
@click.option('--value', prompt=True, help='Detail value')
def add(item_id, key, value):
    """Add a new item detail."""
    crud = ItemDetailCRUD()
    detail = crud.add_detail(item_id, key, value)
    click.echo(f"Item detail added: id={detail.id}, item_id={detail.item_id}, key={detail.key}, value={detail.value}")

@item_detail.command('list')
@click.option('--item-id', type=int, default=None, help='Filter by item ID')
def list_details(item_id):
    """List item details."""
    crud = ItemDetailCRUD()
    details = crud.list_details(item_id)
    if not details:
        click.echo("No item details found.")
    else:
        click.echo(f"{'ID':<4} {'Item ID':<8} {'Key':<16} {'Value'}")
        click.echo('-' * 60)
        for d in details:
            click.echo(f"{d.id:<4} {d.item_id:<8} {d.key[:15]:<16} {d.value}")

@item_detail.command()
@click.argument('detail_id', type=int)
@click.option('--key', help='New key')
@click.option('--value', help='New value')
def edit(detail_id, key, value):
    """Edit an item detail."""
    crud = ItemDetailCRUD()
    updated = crud.edit_detail(detail_id, key, value)
    if updated:
        click.echo("Item detail updated.")
    else:
        click.echo("Item detail not found or nothing to update.")

@item_detail.command()
@click.argument('detail_id', type=int)
def delete(detail_id):
    """Delete an item detail."""
    crud = ItemDetailCRUD()
    deleted = crud.delete_detail(detail_id)
    if deleted:
        click.echo("Item detail deleted.")
    else:
        click.echo("Item detail not found.")
