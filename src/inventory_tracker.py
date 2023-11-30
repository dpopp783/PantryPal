from inventory_entry import InventoryEntry, Ingredient
from typing import List, Dict
import json
import datetime


class InventoryTracker:

    def __init__(self):
        self.inventory: Dict[str, InventoryEntry] = dict()
    
    def __str__(self):
        return ",".join(map(lambda i: i.ingredient.name, self.inventory.values()))

    def add_entry(self, ie: InventoryEntry):
        self.inventory[str(ie.ingredient.id)] = ie

    def remove_entry(self, id: str):
        self.inventory.pop(id)

    def modify_entry(self, id: str, new_name: str, new_quantity: float, new_unit: str, new_exp_date: datetime.date):
        self.remove_entry(id)
        self.add_entry(InventoryEntry(Ingredient(new_name, int(id)), new_quantity, new_unit, new_exp_date))


    def deduct_ingredients(self, ids: List, quantities: List, units: List):
        for id, quantity, unit in zip(ids, quantities, units):
            self.inventory[id].deduct(quantity, unit)

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.to_dict() for ie in self.inventory.values()})
    
    def to_dict(self):
        return {str(ie.ingredient.id): ie.to_dict() for ie in self.inventory.values()}
