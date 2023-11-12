from inventory_entry import InventoryEntry
from typing import List
import json


class InventoryTracker:

    def __init__(self):
        self.inventory: List[InventoryEntry] = []
    
    def __str__(self):
        return ",".join(map(lambda i: i.name, self.inventory))

    def json(self):
        return json.dumps([ie.json() for ie in self.inventory])
