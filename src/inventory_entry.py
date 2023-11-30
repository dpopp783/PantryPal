from dataclasses import dataclass
from datetime import date, datetime
from config import api_key
import requests
import json
import csv


class PantryPalIngredientIDMap(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PantryPalIngredientIDMap, cls).__new__(cls)
            cls.instance.idMap = dict()
            with open('top-1k-ingredients.csv') as ingredients:
                reader = csv.reader(ingredients, delimiter=';')
                for row in reader:
                    ing_name, ing_id = row
                    cls.instance.idMap[ing_id] = ing_name
        return cls.instance

    def get_id(self, name: str):
        # TODO store these 1k top ingredients in a DB instead of dict
        if name.lower().strip() in self.idMap.values():
            print("NO REQ")
            return int(list(self.idMap.keys())[list(self.idMap.values()).index(name.lower().strip())])
        print("REQUESTED")
        url = f"https://api.spoonacular.com/food/ingredients/search/?apiKey={api_key}&query={name}&number=1"
        r = requests.get(url)
        assert r.status_code == 200
        # TODO error handling if there are no results
        return int(r.json()['results'][0]['id'])



@dataclass
class Ingredient:
    name: str
    id: int


def convert(ingredient: str, source_amount: float, source_unit: str, target_unit: str):

    url = f"https://api.spoonacular.com/recipes/convert?apiKey={api_key}&ingredientName={ingredient}&sourceAmount={source_amount}&sourceUnit={source_unit}&targetUnit={target_unit}"
    r = requests.get(url)

    # TODO error handling
    assert r.status_code == 200

    return r.json()["targetAmount"]


class InventoryEntry: 

    def __init__(self, ingredient: Ingredient, quantity: float = 0, unit: str = "", expiration_date: date | str = None):
        self._ingredient = ingredient
        self._quantity = quantity
        self._unit = unit
        # TODO design issue: if multiple units of an ingredient have different expiration dates, how do we represent that?
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        self._expiration_date = expiration_date

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def quantity(self):
        return self._quantity

    @property
    def unit(self):
        return self._unit

    @property
    def expiration_date(self):
        return self._expiration_date

    def deduct(self, amount, unit) -> float:
        if unit != self._unit:
            amount = convert(self._ingredient.name, amount, unit, self._unit)

        # TODO error handling
        assert self._quantity >= amount

        self._quantity -= amount

        return self._quantity

    def add(self, amount, unit):
        if unit != self._unit:
            amount = convert(self._ingredient.name, amount, unit, self._unit)
            print(amount)
        self._quantity += amount

    def jsonify(self):
        return json.dumps({"ingredient": {"name": self._ingredient.name, "id": self._ingredient.id},
                           "quantity": self._quantity,
                           "unit": self._unit,
                           "expiration_date": self._expiration_date.strftime('%Y-%m-%d') if self._expiration_date is not None else ""})
    
    def to_dict(self):
        return {"ingredient": {"name": self._ingredient.name, "id": self._ingredient.id},
                "quantity": self._quantity,
                "unit": self._unit,
                "expiration_date": self._expiration_date.strftime('%Y-%m-%d') if self._expiration_date is not None else ""}
