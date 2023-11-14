import sys
import pytest
from inventory_entry import InventoryEntry, Ingredient
from inventory_tracker import InventoryTracker

sys.path.append('src')


# Test for InventoryTracker class
class TestInventoryTracker:

    def test_add_item_to_inventory(self):
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_entry(InventoryEntry(Ingredient("Butter", 1), 5, "tbsp"))
        assert inventory_tracker.inventory["1"].quantity == 5

    def test_remove_item_from_inventory(self):
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_entry(InventoryEntry(Ingredient("Butter", 1), 5))
        inventory_tracker.remove_entry("1")
        assert "1" not in inventory_tracker.inventory.keys()

    def test_remove_non_existent_item(self):
        inventory_tracker = InventoryTracker()
        with pytest.raises(KeyError):
            inventory_tracker.remove_entry("1")