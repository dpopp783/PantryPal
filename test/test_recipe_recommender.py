import sys
import pytest
from recipe_recommender import Recipe, RecipeRecommender
from inventory_entry import InventoryEntry, Ingredient
from inventory_tracker import InventoryTracker
import json

sys.path.append('src')


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
        flour = InventoryEntry(Ingredient("Flour", 1), 2, "cups")
        sugar = InventoryEntry(Ingredient("Sugar", 2), 1, "cup")
        ingredients = [flour, sugar]
        inventory_tracker = InventoryTracker()
        inventory_tracker.add_entry(flour)
        inventory_tracker.add_entry(sugar)
        
        recipe = Recipe("1", "Pancakes", ingredients)
        recipe_json_str = recipe.jsonify(inventory_tracker)
        recipe_json = json.loads(recipe_json_str)
        assert recipe_json["usedIngredients"] == [{"ingredient": {"id": 1, "name": "Flour"}, "quantity": 2, "unit": "cups"},
                                                  {"ingredient": {"id": 2, "name": "Sugar"}, "quantity": 1, "unit": "cup"}]
        assert recipe_json["missedIngredients"] == []

    def test_recipe_with_no_ingredients(self):
        recipe = Recipe("1", "Water", [])
        inventory_tracker = InventoryTracker()
        recipe_json = recipe.jsonify(inventory_tracker)
        assert recipe_json["usedIngredients"] == []
        assert recipe_json["missedIngredients"] == []

