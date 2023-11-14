from flask import *

# import config
from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient
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


inv_tracker = InventoryTracker()
rice = InventoryEntry(Ingredient("Rice", 1), 1.0, "cup", datetime.datetime.strptime("2023-11-01", "%Y-%m-%d").date())
inv_tracker.add_entry(rice)

next_id = 2


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
    global next_id
    print(request.form)
    if request.method == "POST":
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        new_ingredient = InventoryEntry(Ingredient(name, next_id), quantity, unit, exp_date)
        inv_tracker.add_entry(new_ingredient)
        print(inv_tracker.jsonify())
    next_id += 1
    return redirect("/ingredients")

@app.route("/ingredients/modify", methods=["POST"])
def ingredients_modify():
    return render_template("ingredients.html")

@app.route("/ingredients/remove", methods=["POST"])
def ingredients_remove():
    return render_template("ingredients.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/shoppinglist")
def shoppinglist():

    test = [InventoryEntry(Ingredient("Rice", 1),16,"cup"), InventoryEntry(Ingredient("Flour", 2),24,"oz")]
    return render_template("shoppinglist.html", shoppinglist=test, shoppinglist_JSON='{"1":{"ingredient":{"name":"Rice", "id":1}, "quantity":16, "unit":"cup"}, "2":{"ingredient":{"name":"Flour", "id":2}, "quantity":24, "unit":"oz"}}')

@app.route("/ingredients/data")
def get_ingredient_data():
    # TODO: Add ingredients JSON for users to add ingredients from
    data = {}
    return jsonify(data)