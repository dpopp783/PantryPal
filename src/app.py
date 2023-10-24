from flask import *
from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient
from datetime import date

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/ingredients")
def ingredients():
    test = InventoryTracker()

    item1 = InventoryEntry(Ingredient("Rice", 1), 3, "cup", date(2023, 11, 1))
    item2 = InventoryEntry(Ingredient("Flour", 2), 4, "cup", date(2023, 12, 1))
    item3 = InventoryEntry(Ingredient("Cheese", 3), 5, "cup", date(2023, 12, 24))

    test.inventory = [item1, item2, item3]

    return render_template("ingredients.html", data = test.inventory)

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/shoppinglist")
def shoppinglist():
    return render_template("shoppinglist.html")