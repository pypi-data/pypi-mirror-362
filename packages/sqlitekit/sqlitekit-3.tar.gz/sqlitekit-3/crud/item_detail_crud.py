from dao.item_detail_dao import ItemDetailDAO

class ItemDetailCRUD:
    def __init__(self):
        self.dao = ItemDetailDAO()

    def add_detail(self, item_id, key, value, is_active=True):
        return self.dao.add_detail(item_id, key, value, is_active)

    def get_detail(self, detail_id):
        return self.dao.get_detail(detail_id)

    def list_details(self, item_id=None):
        return self.dao.list_details(item_id)

    def list_disabled_details(self, item_id=None):
        return self.dao.list_disabled_details(item_id)

    def enable_detail(self, detail_id):
        return self.dao.enable_detail(detail_id)

    def disable_detail(self, detail_id):
        return self.dao.disable_detail(detail_id)

    def edit_detail(self, detail_id, key=None, value=None):
        return self.dao.edit_detail(detail_id, key, value)

    def delete_detail(self, detail_id):
        return self.dao.delete_detail(detail_id)
