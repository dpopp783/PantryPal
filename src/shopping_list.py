from inventory_entry import InventoryEntry, Ingredient, PantryPalIngredientIDMap
from typing import Dict
import json


class ShoppingList:

    def __init__(self):
        self.shopping_list: Dict[str, InventoryEntry] = dict()

    def _add_item(self, item: InventoryEntry):
        self.shopping_list[str(item.ingredient.id)] = item

    def add_item(self, name: str, quantity: float, unit: str):
        idMap = PantryPalIngredientIDMap()
        newEntry = InventoryEntry(Ingredient(name, idMap.get_id(name)), quantity, unit, None)
        self._add_item(newEntry)

    def remove_item(self, id: str):
        self.shopping_list.pop(id)

    def modify_item(self, id: str, new_name: str, new_quantity: float, new_unit: str):
        self.remove_item(id)
        self._add_item(InventoryEntry(Ingredient(new_name, int(id)), new_quantity, new_unit))

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.to_dict() for ie in self.shopping_list.values()})
