import requests
from config import api_key
from inventory_entry import InventoryEntry, Ingredient
from inventory_tracker import InventoryTracker
from typing import List, Optional
import json
from util import check_status_code


class Recipe:

    def __init__(self, id: str, name: str, ingredients: List[InventoryEntry], image_url: Optional[str] = None):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.ingredients = ingredients

    def to_dict(self, inv_tracker: InventoryTracker):
        data = dict()
        data["id"] = self.id
        data["name"] = self.name
        data["image"] = self.image_url
        usedIngredients = []
        missedIngredients = []
        for ingredient in self.ingredients:
            # print(ingredient.unit)
            ing_dict = ingredient.to_dict()
            ing_dict.pop("expiration_date")
            if str(ingredient.ingredient.id) in inv_tracker.inventory.keys():
                # TODO check if they have enough of the ingredient
                # if not inv_tracker.have_enough(ingredient.ingredient.id, ingredient.quantity, ingredient.unit):
                #     missedIngredients.append(ing_dict)
                # else:
                usedIngredients.append(ing_dict)
            else:
                missedIngredients.append(ing_dict)
        data["usedIngredients"] = usedIngredients
        data["missedIngredients"] = missedIngredients
        return data

    def jsonify(self, inv_tracker: InventoryTracker):
        return json.dumps(self.to_dict(inv_tracker))


class RecipeRecommender:

    def __init__(self):
        self.recommendations = []

    def get_recommendations(self, inv_tracker: InventoryTracker, num_recipes: int):
        ingredients = inv_tracker.__str__()
        url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}&number={num_recipes}&ranking=2&ignorePantry=false&instructionsRequired=true"
        r = requests.get(url)
        check_status_code(r)

        self.recommendations = []

        # TODO figure out how to get recipe instructions

        for j in r.json():
            id = j["id"]
            name = j["title"]
            image_url = j["image"]
            ingredients = []
            for ing in j["missedIngredients"]:
                ingredients.append(InventoryEntry(Ingredient(ing["name"], ing["id"]), ing["amount"], ing["unit"]))
            for ing in j["usedIngredients"]:
                ingredients.append(InventoryEntry(Ingredient(ing["name"], ing["id"]), ing["amount"], ing["unit"]))
            self.recommendations.append(Recipe(id, name, ingredients, image_url))
        return self.recommendations

    def jsonify(self, inv_tracker: InventoryTracker):
        return json.dumps({rec.id: rec.to_dict(inv_tracker) for rec in self.recommendations})


    def get_url(title: str, id: int):
        return "https://spoonacular.com/recipes/" + {"-".join(title.lower().split(" "))} + "-" + str(id)