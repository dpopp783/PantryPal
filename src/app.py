from flask import *

import config
from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient
from shopping_list import ShoppingList
from datetime import date
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv
from forms import AddInventoryEntry, AddShoppingListEntry

conn = psycopg2.connect(
    user='postgres',
    password=config.postgres_pw,
    host='localhost',
    dbname='pantry',
    port=5433)


# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS ingredient;')
cur.execute('CREATE TABLE ingredient (id int PRIMARY KEY,'
            'name varchar(100) NOT NULL);')

with open('top-1k-ingredients.csv') as ingredients:
    reader = csv.reader(ingredients, delimiter=';')
    for row in reader:
        ing_name, ing_id = row
        if ing_name.find("'") != -1:
            # TODO there is a syntax error if you try to insert a string into the postgresql db that has a ' in it, haven't yet figured out how to escape it
            continue
        cur.execute(f"INSERT INTO ingredient(id, name) VALUES({ing_id}, '{ing_name}')")

# Create inventory_entry table
cur.execute('DROP TABLE IF EXISTS inventory_entry;')
cur.execute('CREATE TABLE inventory_entry (id serial PRIMARY KEY,'
            'ingredient_id int NOT NULL REFERENCES ingredient(id),'
            'amount float NOT NULL,'
            f'unit varchar({config.MAX_INGREDIENT_NAME_LENGTH}) NOT NULL,'
            'expiration_date date DEFAULT CURRENT_DATE + 7);'
            )
cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(20444, 10, 'cup','2023-12-1')")
cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(20081, 8, 'cup','2023-12-24')")
cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(1009, 2, 'cup','2023-11-1')")

inventory_tracker = InventoryTracker()

cur.execute('SELECT * FROM inventory_entry')
entries = cur.fetchall()

inventory = []
for id, ing_id, amount, unit, date in entries:
    cur.execute(f'SELECT name FROM ingredient WHERE id={ing_id}')
    ing_name = cur.fetchall()[0][0]
    inventory.append(InventoryEntry(Ingredient(ing_name, ing_id), amount, unit, date))

inventory_tracker.inventory = inventory

# Create shopping_list table
cur.execute('DROP TABLE IF EXISTS shopping_list;')
cur.execute('CREATE TABLE shopping_list (id serial PRIMARY KEY,'
            'ingredient_id int NOT NULL REFERENCES ingredient(id),'
            'amount float NOT NULL,'
            f'unit varchar({config.MAX_INGREDIENT_NAME_LENGTH}) NOT NULL);'
            )
cur.execute("INSERT INTO shopping_list(ingredient_id, amount, unit) VALUES(20444, 10, 'cup')")
cur.execute("INSERT INTO shopping_list(ingredient_id, amount, unit) VALUES(20081, 8, 'cup')")
cur.execute("INSERT INTO shopping_list(ingredient_id, amount, unit) VALUES(1009, 2, 'cup')")

shopping_list = ShoppingList()

cur.execute('SELECT * FROM shopping_list')
entries = cur.fetchall()

sl = []
for id, ing_id, amount, unit in entries:
    cur.execute(f'SELECT name FROM ingredient WHERE id={ing_id}')
    ing_name = cur.fetchall()[0][0]
    sl.append(InventoryEntry(Ingredient(ing_name, ing_id), amount, unit))

shopping_list.shopping_list = sl

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("dashboard.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/ingredients")
def ingredients():
    # TODO: Add another arg called inventory_JSON, set it equal to the JSON representation of the InventoryTracker
    return render_template("ingredients.html", inventory=inventory_tracker.inventory)

"""
@app.route("/ingredients/add")
def add_ingredient():
    form = AddInventoryEntry()

    if form.validate_on_submit():
        # get id
        new_inventory_entry = InventoryEntry(Ingredient(form.ingredient_name, <id>), form.quantity, form.unit, form.exp_date)
        inventory_tracker.add_entry(new_inventory_entry)
    pass
    #return render_template(,  form=form)
"""

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/shoppinglist")
def shoppinglist():
    return render_template("shoppinglist.html", shoppinglist=shopping_list.shopping_list, shoppinglist_JSON=shopping_list.json())
