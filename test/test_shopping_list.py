import sys
sys.path.append('src')
import pytest
from datetime import date
from inventory_entry import InventoryEntry, Ingredient, convert
from shopping_list import ShoppingList

# Fixtures for testing
@pytest.fixture
def ingredient():
    return Ingredient('Apple', 1)

@pytest.fixture
def inventory_entry(ingredient):
    return InventoryEntry(ingredient, 10, 'kg', date.today())

@pytest.fixture
def shopping_list():
    return ShoppingList()

# Tests for InventoryEntry class
def test_inventory_entry_initialization(inventory_entry, ingredient):
    assert inventory_entry.ingredient == ingredient
    assert inventory_entry.quantity == 10
    assert inventory_entry.unit == 'kg'
    assert inventory_entry.expiration_date == date.today()

def test_inventory_entry_deduct(inventory_entry):
    inventory_entry.deduct(2, 'kg')
    assert inventory_entry.quantity == 8

def test_inventory_entry_to_dict(inventory_entry):
    result = inventory_entry.to_dict()
    assert result == {
        "ingredient": {"name": "Apple", "id": 1},
        "quantity": 10,
        "unit": "kg",
        "expiration_date": date.today().strftime('%Y-%m-%d')
    }

# Tests for ShoppingList class
def test_shopping_list_initialization(shopping_list):
    assert shopping_list.shopping_list == {}

def test_add_item(shopping_list, inventory_entry):
    shopping_list.add_item(inventory_entry)
    assert str(inventory_entry.ingredient.id) in shopping_list.shopping_list
    assert shopping_list.shopping_list[str(inventory_entry.ingredient.id)] == inventory_entry

def test_remove_item(shopping_list, inventory_entry):
    shopping_list.add_item(inventory_entry)
    shopping_list.remove_item(str(inventory_entry.ingredient.id))
    assert str(inventory_entry.ingredient.id) not in shopping_list.shopping_list

def test_modify_item(shopping_list, inventory_entry):
    shopping_list.add_item(inventory_entry)
    shopping_list.modify_item(str(inventory_entry.ingredient.id), 'Banana', 5, 'kg')
    modified_item = shopping_list.shopping_list[str(inventory_entry.ingredient.id)]
    assert modified_item.ingredient.name == 'Banana'
    assert modified_item.quantity == 5
    assert modified_item.unit == 'kg'

def test_jsonify(shopping_list, inventory_entry):
    shopping_list.add_item(inventory_entry)
    json_output = shopping_list.jsonify()
    assert inventory_entry.ingredient.name in json_output
    assert str(inventory_entry.quantity) in json_output
    assert inventory_entry.unit in json_output
