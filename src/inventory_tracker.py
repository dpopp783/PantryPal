from inventory_entry import InventoryEntry


class InventoryTracker:

    def __init__(self):
        self.inventory = []
    
    def __str__(self):
        return ",".join(map(lambda i: i.name, self.inventory))
