from inventory_entry import InventoryEntry
from typing import List
import json


class ShoppingList:

    def __init__(self):
        self.shopping_list: List[InventoryEntry] = []

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.jsonify() for ie in self.shopping_list})
