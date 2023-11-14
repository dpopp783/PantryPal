// Recipe.js

class Recipe {
    constructor(name, ingredients, steps) {
        this.name = name;
        this.ingredients = ingredients; // Array of {ingredientName, quantity, unit}
        this.steps = steps; // Array of strings
    }
}

class RecipeManager {
    constructor() {
        this.recipes = [];
        // Load recipes from local storage or database here
    }

    suggestRecipes(pantry) {
        // Logic to suggest recipes based on pantry items
        // pantry: Array of {ingredientName, quantity, unit}
    }

    addRecipe(recipe) {
        // Add a new recipe
        // recipe: instance of Recipe
        this.recipes.push(recipe);
        // Save to local storage or database
    }

    modifyRecipe(recipeName, newRecipe) {
        // Modify an existing recipe
        // Find recipe by name and update it with newRecipe details
    }

    deleteRecipe(recipeName) {
        // Delete a recipe by name
        this.recipes = this.recipes.filter(recipe => recipe.name !== recipeName);
        // Update local storage or database
    }

    getRecipeDetails(recipeName) {
        // Return details of a specific recipe
        return this.recipes.find(recipe => recipe.name === recipeName);
    }

    cookRecipe(recipeName, pantryManager) {
        // Deduct ingredients from pantry when a recipe is cooked
        const recipe = this.getRecipeDetails(recipeName);
        if (recipe) {
            recipe.ingredients.forEach(ingredient => {
                pantryManager.deductIngredient(ingredient.ingredientName, ingredient.quantity);
            });
        }
    }
}


// Event listener for opening the add recipe modal
document.getElementById('addRecipe').addEventListener('click', () => {
    // Clear the form fields
    document.getElementById('recipeName').value = '';
    document.getElementById('recipeIngredients').value = '';
    document.getElementById('recipeSteps').value = '';
    // Open the modal (Bootstrap 5 handles this automatically)
});

// Event listener for saving the new recipe
document.getElementById('saveRecipe').addEventListener('click', () => {
    const name = document.getElementById('recipeName').value.trim();
    const ingredientsInput = document.getElementById('recipeIngredients').value.trim();
    const stepsInput = document.getElementById('recipeSteps').value.trim();

    if (name && ingredientsInput && stepsInput) {
        const ingredients = ingredientsInput.split(',').map(ingredient => {
            // Split each ingredient into its name, quantity, and unit
            // This depends on your ingredient format
            return {
                ingredientName: ingredient, // Modify as per your format
                quantity: 1, // Modify as per your format
                unit: 'unit' // Modify as per your format
            };
        });

        const steps = stepsInput.split('.').map(step => step.trim()).filter(step => step);

        // Create a new Recipe instance
        const newRecipe = new Recipe(name, ingredients, steps);

        // Add to RecipeManager and update the UI
        // Assuming you have an instance of RecipeManager
        recipeManager.addRecipe(newRecipe);
        updateRecipeListUI();

        // Close the modal (Bootstrap 5 handles this automatically)
    } else {
        // Handle error: all fields are required
    }
});

// Utility function to update the recipe list in the UI
function updateRecipeListUI() {
    // Logic to update the recipe list in the UI goes here
    // For example, you could iterate over recipeManager.recipes and 
    // append each recipe's details to a DOM element
}

// Initialize the RecipeManager and update the UI on load
const recipeManager = new RecipeManager();
updateRecipeListUI();

// Additional functions and event listeners...