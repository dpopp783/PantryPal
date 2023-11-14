from dataclasses import dataclass
from datetime import date
# from config import api_key
import requests
import json


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

    def __init__(self, ingredient: Ingredient, quantity: float = 0, unit: str = "", expiration_date: date = None):
        self._ingredient = ingredient
        self._quantity = quantity
        self._unit = unit
        # TODO design issue: if multiple units of an ingredient have different expiration dates, how do we represent that?
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
            quantity = convert(self._ingredient.name, amount, unit, self._unit)

        # TODO error handling
        assert self._quantity >= amount

        self._quantity -= amount

        return self._quantity

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
