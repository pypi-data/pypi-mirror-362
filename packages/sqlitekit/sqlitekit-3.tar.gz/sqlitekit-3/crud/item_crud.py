from dao.item_dao import ItemDAO

class ItemCRUD:
    def __init__(self):
        self.dao = ItemDAO()

    def add_item(self, name, description, tags, category_id, is_active=True):
        return self.dao.add_item(name, description, tags, category_id, is_active)

    def get_item(self, item_id):
        return self.dao.get_item(item_id)

    def list_items(self):
        return self.dao.list_items()

    def list_disabled_items(self):
        return self.dao.list_disabled_items()

    def enable_item(self, item_id):
        return self.dao.enable_item(item_id)

    def disable_item(self, item_id):
        return self.dao.disable_item(item_id)

    def edit_item(self, item_id, name=None, description=None, tags=None, category_id=None, is_active=None):
        return self.dao.edit_item(item_id, name, description, tags, category_id, is_active)

    def delete_item(self, item_id):
        return self.dao.delete_item(item_id)
