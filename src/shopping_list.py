from inventory_entry import InventoryEntry
from typing import Dict
import json


class ShoppingList:

    def __init__(self):
        self.shopping_list: Dict[str, InventoryEntry] = dict()

    def add_item(self, item: InventoryEntry):
        self.shopping_list[str(item.ingredient.id)] = item

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.to_dict() for ie in self.shopping_list.values()})
