import inventory_entry
from inventory_entry import InventoryEntry, Ingredient, PantryPalIngredientIDMap
from typing import List, Dict
import json
import datetime

from data_util import *

class InventoryTracker:

    def __init__(self, username: str):
        self.inventory: Dict[str, InventoryEntry] = dict()

        data = get_data(username)
        inventory = data["inventory"]
        for item in inventory.values():
            self.inventory[item["ingredient"]["id"]] = InventoryEntry(
                Ingredient(item["ingredient"]["name"], item["ingredient"]["id"]),
                item["quantity"],
                item["unit"],
                item["expiration_date"]
            )
    
    def __str__(self):
        return ",".join(map(lambda i: i.ingredient.name, self.inventory.values()))

    def _add_entry(self, ie: InventoryEntry):
        self.inventory[int(ie.ingredient.id)] = ie

    def add_entry(self, name: str, quantity: float, unit: str, exp_date: datetime.date):
        idMap = PantryPalIngredientIDMap()
        ing_id = idMap.get_id(name)
        if str(ing_id) not in self.inventory.keys():
            newEntry = InventoryEntry(Ingredient(name, ing_id), quantity, unit, exp_date)
            self._add_entry(newEntry)
        else:
            self.inventory[str(ing_id)].add(quantity, unit)

    def remove_entry(self, id: str):
        self.inventory.pop(int(id))

    def get_entry(self, id: str):
        return self.inventory.get(int(id))

    def have_enough(self, id: int, needed_quantity: float, needed_unit: str):
        entry = self.get_entry(str(id))
        if needed_unit != entry.unit:
            print(needed_unit)
            print(entry.unit)
            needed_quantity = inventory_entry.convert(entry.ingredient.name, needed_quantity, needed_unit, entry.unit)
        return entry.quantity >= needed_quantity

    def modify_entry(self, id: str, new_name: str, new_quantity: float, new_unit: str, new_exp_date: datetime.date):
        self.remove_entry(int(id))
        self._add_entry(InventoryEntry(Ingredient(new_name, int(id)), new_quantity, new_unit, new_exp_date))

    def deduct_ingredients(self, ids: List, quantities: List, units: List):
        for id, quantity, unit in zip(ids, quantities, units):
            try:
                self.inventory[id].deduct(quantity, unit)
            except ValueError as e:
                print(str(e))

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.to_dict() for ie in self.inventory.values()})
    
    def to_dict(self):
        return {str(ie.ingredient.id): ie.to_dict() for ie in self.inventory.values()}
