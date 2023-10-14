from inventory_entry import InventoryEntry


class InventoryTracker:

    def __init__(self):
        self.inventory = []

    def inventoryToString(self):
        return ",".join(map(lambda i: i.name, self.inventory))
