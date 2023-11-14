import requests
from config import api_key
from inventory_entry import InventoryEntry, Ingredient
from inventory_tracker import InventoryTracker
from typing import List, Optional
import json


class Recipe:

    def __init__(self, id: str, name: str, ingredients: List[InventoryEntry], image_url=Optional[str]):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.ingredients = ingredients

    def jsonify(self, inv_tracker: InventoryTracker):
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        usedIngredients = []
        missedIngredients = []
        for ingredient in self.ingredients:
            if ingredient.id in inv_tracker.inventory.keys():
                # TODO check if they have enough of the ingredient
                usedIngredients.append(ingredient.jsonify())
            else:
                missedIngredients.append(ingredient.jsonify())
        data["usedIngredients"] = usedIngredients
        data["missedIngredients"] = missedIngredients


class RecipeRecommender:

    def __init__(self):
        self.recommendations = []

    def get_recommendations(self, ingredients: str, num_recipes: int):
        url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}&number={num_recipes}&ranking=2&ignorePantry=False"
        r = requests.get(url)
        assert r.status_code == 200

        self.recommendations = []

        for j in r.json():
            id = j["id"]
            name = j["name"]
            image_url = j["image"]
            ingredients = []
            for ing in j["missedIngredients"]:
                ingredients.append(InventoryEntry(Ingredient(ing["name"], ing["id"]), ing["amount"], ing["unit"]))
            for ing in j["usedIngredients"]:
                ingredients.append(InventoryEntry(Ingredient(ing["name"], ing["id"]), ing["amount"], ing["unit"]))
            self.recommendations.append(Recipe(id, name, image_url, ingredients))
        return self.recommendations

    def jsonify(self, inv_tracker: InventoryTracker):
        return json.dumps({rec.id: rec.jsonify(inv_tracker) for rec in self.recommendations})
