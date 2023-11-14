from unittest.mock import patch, Mock
from your_module import InventoryEntry, convert, Ingredient, SpoonacularApiClient
import unittest
from datetime import date

class TestInventoryEntry(unittest.TestCase):

    def setUp(self):
        #Inject trial SpoonacularApiClient
        self.mock_spoonacular_api_client = Mock()
        convert.spoonacular_api_client = self.mock_spoonacular_api_client

    @patch('your_module.requests.get')
    def test_convert_ounces_to_grams(self, mock_requests_get):
        #Testing convert() (converts ounces to grams)
        # Spoonacular to return a conversion factor of 5.0
        self.mock_spoonacular_api_client.get.return_value = {"targetAmount": 5.0}

        # Convert() method with 10.0 ounces as the input
        result = convert("carrot", 10.0, "ounces", "grams")

        # Result  5.0 grams
        self.assertEqual(result, 5.0)

    def test_convert_invalid_unit_of_measurement(self):
        #convert() method throwing an exception (ValueError exception)
        with self.assertRaises(ValueError):
            convert("carrot", 10.0, "invalid_unit", "grams")

    def test_inventory_entry_properties(self):
        #InventoryEntry class set correctly
        ingredient = Ingredient(name="carrot", id=1)

        # InventoryEntry object, quantity of 100g, expiration date of 2023-12-31
        entry = InventoryEntry(ingredient, quantity=100, unit="grams", expiration_date=date(2023, 12, 31))

        self.assertEqual(entry.ingredient, ingredient)
        self.assertEqual(entry.quantity, 100)
        self.assertEqual(entry.unit, "grams")
        self.assertEqual(entry.expiration_date, date(2023, 12, 31))

    def test_deduct(self):
        # Create an Ingredient object for deduct() method
        ingredient = Ingredient(name="carrot", id=1)

        #InventoryEntry object, quantity of 100g, expiration date of 2023-12-31
        entry = InventoryEntry(ingredient, quantity=100, unit="grams", expiration_date=date(2023, 12, 31))

        # Deduct 50 grams from InventoryEntry 
        new_quantity = entry.deduct(50, "grams")
        # Check new quantity is 50 grams
        self.assertEqual(new_quantity, 50)

if __name__ == '__main__':
    unittest.main()

