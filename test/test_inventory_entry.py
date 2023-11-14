import sys
import json
import pytest 
from datetime import date 


def test_convert_valid_ingredient():
    """Test that the convert() function returns the correct conversion for a valid ingredient."""
    # Arrange
    ingredient = "flour"
    source_amount = 100
    source_unit = "grams"
    target_unit = "cups"

    # Act
    target_amount = convert(ingredient, source_amount, source_unit, target_unit)

    # Assert
    assert target_amount == 2.204622621848776

def test_convert_invalid_ingredient():
    """Test that the convert() function raises an exception when given an invalid ingredient."""
    # Arrange
    ingredient = "invalid_ingredient"
    source_amount = 100
    source_unit = "grams"
    target_unit = "cups"

    # Act
    with pytest.raises(ValueError):
        convert(ingredient, source_amount, source_unit, target_unit)

# Test the InventoryEntry class

def test_inventory_entry_init():
    """Test that the InventoryEntry constructor initializes the object correctly."""
    # Arrange
    ingredient = Ingredient(name="flour", id=1)
    quantity = 100
    unit = "grams"
    expiration_date = date(2023, 11, 15)

    # Act
    inventory_entry = InventoryEntry(ingredient, quantity, unit, expiration_date)

    # Assert
    assert inventory_entry.ingredient == ingredient
    assert inventory_entry.quantity == quantity
    assert inventory_entry.unit == unit
    assert inventory_entry.expiration_date == expiration_date

def test_inventory_entry_deduct_valid_amount():
    """Test that the InventoryEntry.deduct() method deducts the specified amount of the ingredient correctly."""
    # Arrange
    inventory_entry = InventoryEntry(Ingredient(name="flour", id=1), 100, "grams")
    amount = 50
    unit = "grams"

    # Act
    new_quantity = inventory_entry.deduct(amount, unit)

    # Assert
    assert new_quantity == 50

# ... (similarly, implement other test functions)

if __name__ == "__main__":
    pytest.main()
