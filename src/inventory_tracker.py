from inventory_entry import InventoryEntry
from typing import List, Dict
import json


class InventoryTracker:

    def __init__(self):
        self.inventory: Dict[str, InventoryEntry] = dict()
    
    def __str__(self):
        return ",".join(map(lambda i: i.name, self.inventory))

    def add_entry(self, ie: InventoryEntry):
        self.inventory[ie.ingredient.id] = ie

    def deduct_ingredients(self, ids: List, quantities: List, units: List):
        for id, quantity, unit in zip(ids, quantities, units):
            self.inventory[id].deduct(quantity, unit)

    def jsonify(self):
        return json.dumps({ie.ingredient.id: ie.jsonify() for ie in self.inventory.values()})
