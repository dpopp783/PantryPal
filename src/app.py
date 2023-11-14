from flask import *

# import config
from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient
from shopping_list import ShoppingList
from recipe_recommender import Recipe, RecipeRecommender
import datetime
#import psycopg2
#from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv

# conn = psycopg2.connect(
#     user='postgres',
#     password=config.postgres_pw,
#     host='localhost',
#     dbname='pantry',
#     port=5433)


# # Open a cursor to perform database operations
# cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS ingredient;')
# cur.execute('CREATE TABLE ingredient (id int PRIMARY KEY,'
#             'name varchar(100) NOT NULL);')

# with open('src/top-1k-ingredients.csv') as ingredients:
#     reader = csv.reader(ingredients, delimiter=';')
#     for row in reader:
#         ing_name, ing_id = row
#         if ing_name.find("'") != -1:
#             # TODO there is a syntax error if you try to insert a string into the postgresql db that has a ' in it, haven't yet figured out how to escape it
#             continue
#         cur.execute(f"INSERT INTO ingredient(id, name) VALUES({ing_id}, '{ing_name}')")

# # Create inventory_entry table
# cur.execute('DROP TABLE IF EXISTS inventory_entry;')
# cur.execute('CREATE TABLE inventory_entry (id serial PRIMARY KEY,'
#             'ingredient_id int NOT NULL REFERENCES ingredient(id),'
#             'amount float NOT NULL,'
#             'unit varchar(50) NOT NULL,'
#             'expiration_date date DEFAULT CURRENT_DATE + 7);'
#             )
# cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(20444, 10, 'cup','2023-12-1')")
# cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(20081, 8, 'cup','2023-12-24')")
# cur.execute("INSERT INTO inventory_entry(ingredient_id, amount, unit, expiration_date) VALUES(1009, 2, 'cup','2023-11-1')")

app = Flask(__name__)

# Setup test InventoryTracker object
inv_tracker = InventoryTracker()
rice = InventoryEntry(Ingredient("Rice", 1), 1.0, "cup", datetime.datetime.strptime("2023-11-01", "%Y-%m-%d").date())
inv_tracker.add_entry(rice)
next_id_inv = 2

# Setup test ShoppingList object
shop_list = ShoppingList()
rice = InventoryEntry(Ingredient("Rice", 1),16,"cup")
flour = InventoryEntry(Ingredient("Flour", 2),24,"oz")
shop_list.add_item(rice)
shop_list.add_item(flour)
next_id_sl = 3


@app.route("/")
def login():
    return render_template("dashboard.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/ingredients", methods=["GET"])
def ingredients():

    # cur.execute('SELECT * FROM inventory_entry')
    # entries = cur.fetchall()

    inventory = []
    # for id, ing_id, amount, unit, date in entries:
    #     cur.execute(f'SELECT name FROM ingredient WHERE id={ing_id}')
    #     ing_name = cur.fetchall()[0][0]
    #     inventory.append(InventoryEntry(Ingredient(ing_name, ing_id), amount, unit, date))

    # TODO: Add another arg called inventory_JSON, set it equal to the JSON representation of the InventoryTracker
    return render_template("ingredients.html", inventory=inv_tracker.inventory, inventory_JSON=inv_tracker.jsonify())


@app.route("/ingredients/add", methods=["POST"])
def ingredients_add():
    global next_id_inv
    if request.method == "POST":
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        new_ingredient = InventoryEntry(Ingredient(name, next_id_inv), quantity, unit, exp_date)
        inv_tracker.add_entry(new_ingredient)
        print(inv_tracker.jsonify())
    next_id_inv += 1
    return redirect("/ingredients")


@app.route("/ingredients/modify", methods=["POST"])
def ingredients_modify():
    mod_id = request.form["id"]
    new_name = request.form["name"]
    new_quantity = float(request.form["quantity"])
    new_unit = request.form["unit"]
    new_exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
    inv_tracker.modify_entry(mod_id, new_name, new_quantity, new_unit, new_exp_date)
    return redirect("/ingredients")


@app.route("/ingredients/remove", methods=["POST"])
def ingredients_remove():
    inv_tracker.remove_entry(request.form["id"])
    return redirect("/ingredients")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/shoppinglist")
def shoppinglist():
    return render_template("shoppinglist.html", shoppinglist=shop_list.shopping_list.values(), shoppinglist_JSON=shop_list.jsonify())


@app.route("/shoppinglist/add", methods=["POST"])
def add_shoppinglist():
    global next_id_sl
    if request.method == "POST":
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        new_ingredient = InventoryEntry(Ingredient(name, next_id_sl), quantity, unit)
        shop_list.add_item(new_ingredient)
    next_id_sl += 1
    return redirect("/shoppinglist")


@app.route("/shoppinglist/modify", methods=["POST"])
def modify_shoppinglist():
    mod_id = request.form["id"]
    new_name = request.form["name"]
    new_quantity = float(request.form["quantity"])
    new_unit = request.form["unit"]
    shop_list.modify_item(mod_id, new_name, new_quantity, new_unit)
    return redirect("/shoppinglist")


@app.route("/shoppinglist/remove", methods=["POST"])
def remove_shoppinglist():
    shop_list.remove_item(request.form["id"])
    return redirect("/shoppinglist")


@app.route("/shoppinglist/purchase", methods=["POST"])
def purhcase_shoppinglist():
    pur_id = request.form["id"]
    # TODO request expiration date from user when you hit the purchase button
    inv_tracker.add_entry(shop_list.shopping_list[pur_id])
    shop_list.remove_item(pur_id)
    return redirect("/shoppinglist")


@app.route("/ingredients/data")
def get_ingredient_data():
    # TODO: Add ingredients JSON for users to add ingredients from
    data = {}
    return jsonify(data)
