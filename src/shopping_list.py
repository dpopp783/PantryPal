from inventory_entry import InventoryEntry, Ingredient
from typing import Dict
import json


class ShoppingList:

    def __init__(self):
        self.shopping_list: Dict[str, InventoryEntry] = dict()

    def add_item(self, item: InventoryEntry):
        self.shopping_list[str(item.ingredient.id)] = item

    def remove_item(self, id: str):
        self.shopping_list.pop(id)

    def modify_item(self, id: str, new_name: str, new_quantity: float, new_unit: str):
        self.remove_item(id)
        self.add_item(InventoryEntry(Ingredient(new_name, int(id)), new_quantity, new_unit))

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.to_dict() for ie in self.shopping_list.values()})
