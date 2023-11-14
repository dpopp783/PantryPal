import unittest
from src.inventory_entry import Ingredient


def test_initialization():
    a = Ingredient("Rice", 1)
    assert a.id == 1 and a.name == "Rice"


def test_initialization_err():
    a = Ingredient("Rice")


if __name__ == "__main__":
    unittest.main()