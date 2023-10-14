import requests
from config import api_key


class RecipeRecommender:

    def get_recommendations(self, ingredients: str, num_recipes: int):
        url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}&number={num_recipes}&ranking=2&ignorePantry=False"
        r = requests.get(url)
        assert r.status_code == 200
        return r.json()

