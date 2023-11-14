import sys
sys.path.append('src')
import pytest
from recipe_recommender import Recipe, InventoryEntry, Ingredient, InventoryTracker

# Test for Recipe class
class TestRecipe:

    def test_recipe_initialization(self):
        ingredients = [InventoryEntry("1", "Flour", 2), InventoryEntry("2", "Sugar", 1)]
        recipe = Recipe("1", "Pancakes", ingredients)
        assert recipe.id == "1"
        assert recipe.name == "Pancakes"
        assert recipe.ingredients == ingredients
        assert recipe.image_url is None

    def test_jsonify_with_full_inventory(self):
        ingredients = [InventoryEntry("1", "Flour", 2), InventoryEntry("2", "Sugar", 1)]
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_item(Ingredient("1", "Flour"), 2)
        inventory_tracker.add_item(Ingredient("2", "Sugar"), 1)
        
        recipe = Recipe("1", "Pancakes", ingredients)
        recipe_json = recipe.jsonify(inventory_tracker)
        assert recipe_json["usedIngredients"] == [{"id": "1", "name": "Flour"}, {"id": "2", "name": "Sugar"}]
        assert recipe_json["missedIngredients"] == []

# Test for InventoryEntry class
class TestInventoryEntry:

    def test_inventory_entry_initialization(self):
        entry = InventoryEntry("1", "Eggs", 12)
        assert entry.id == "1"
        assert entry.name == "Eggs"
        assert entry.quantity == 12

# Test for Ingredient class
class TestIngredient:

    def test_ingredient_initialization(self):
        ingredient = Ingredient("1", "Milk")
        assert ingredient.id == "1"
        assert ingredient.name == "Milk"

# Test for InventoryTracker class
class TestInventoryTracker:

    def test_add_item_to_inventory(self):
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_item(Ingredient("1", "Butter"), 5)
        assert inventory_tracker.inventory["1"].quantity == 5

    def test_remove_item_from_inventory(self):
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_item(Ingredient("1", "Butter"), 5)
        inventory_tracker.remove_item("1", 3)
        assert inventory_tracker.inventory["1"].quantity == 2

    def test_remove_non_existent_item(self):
        inventory_tracker = InventoryTracker()
        with pytest.raises(KeyError):
            inventory_tracker.remove_item("1", 3)

# Test for error handling and edge cases
class TestErrorHandling:

    def test_invalid_ingredient_quantity(self):
        with pytest.raises(ValueError):
            InventoryEntry("1", "Sugar", -1)

    def test_recipe_with_no_ingredients(self):
        recipe = Recipe("1", "Water", [])
        inventory_tracker = InventoryTracker()
        recipe_json = recipe.jsonify(inventory_tracker)
        assert recipe_json["usedIngredients"] == []
        assert recipe_json["missedIngredients"] == []
