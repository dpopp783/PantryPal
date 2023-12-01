from flask import *

# import config
from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient, PantryPalIngredientIDMap
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
global response

# Setup test InventoryTracker object

idMap = PantryPalIngredientIDMap()
inv_tracker = InventoryTracker()
inv_tracker.add_entry("Rice", 2.0, "cup", datetime.datetime.strptime("2023-12-28", "%Y-%m-%d").date())
inv_tracker.add_entry("Flour", 10.0, "cup", datetime.date(2024, 9, 4))
inv_tracker.add_entry("Sugar", 8.0, "cup", datetime.date(2024, 5, 23))
inv_tracker.add_entry("Apple", 6.0, "large", datetime.date(2023, 11, 18))
inv_tracker.add_entry("Vinegar", 10.0, "cup", datetime.date(2024, 9, 4))
inv_tracker.add_entry("Milk", 8.0, "cup", datetime.date(2024, 5, 23))
inv_tracker.add_entry("Cheese", 6.0, "large", datetime.date(2023, 11, 18))

# Setup test ShoppingList object
shop_list = ShoppingList()
shop_list.add_item("Rice", 16, "cup")
shop_list.add_item("Cheddar", 24, "oz")

# setup test RecipeRecommender object
recipe_recommender = RecipeRecommender()

@app.route("/", methods=["GET"])
def index():
    global response
    try:
        pass
    except Exception as e:
        pass
    return render_template("login.html", response = response)


@app.route("/login", methods=["POST"])
def login():
    global response
    try:
        return redirect("/dashboard")
    except Exception as e:
        return redirect("/")
    

@app.route("/signup", methods=["POST"])
def signup():
    global response
    try:
        return redirect("/dashboard")
    except Exception as e:
        pass
        return redirect("/")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    return render_template("dashboard.html", 
        inventory = inv_tracker.inventory, 
        shoppinglist = shop_list.shopping_list.values(),
        recipe = recipe_recommender.recommendations,
        response = response
        )


@app.route("/ingredients", methods=["GET"])
def ingredients():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "
    
    # cur.execute('SELECT * FROM inventory_entry')
    # entries = cur.fetchall()

    inventory = []
    # for id, ing_id, amount, unit, date in entries:
    #     cur.execute(f'SELECT name FROM ingredient WHERE id={ing_id}')
    #     ing_name = cur.fetchall()[0][0]
    #     inventory.append(InventoryEntry(Ingredient(ing_name, ing_id), amount, unit, date))

    # TODO: Add another arg called inventory_JSON, set it equal to the JSON representation of the InventoryTracker
    return render_template("ingredients.html", inventory=inv_tracker.inventory, inventory_JSON=inv_tracker.jsonify(), response=response)


@app.route("/ingredients/add", methods=["POST"])
def ingredients_add():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    if request.method == "POST":
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
        inv_tracker.add_entry(name, quantity, unit, exp_date)
    return redirect("/ingredients")


@app.route("/ingredients/modify", methods=["POST"])
def ingredients_modify():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    mod_id = request.form["id"]
    new_name = request.form["name"]
    new_quantity = float(request.form["quantity"])
    new_unit = request.form["unit"]
    if len(request.form['expiration_date']):
        new_exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
    else:
        new_exp_date = None
    inv_tracker.modify_entry(mod_id, new_name, new_quantity, new_unit, new_exp_date)
    return redirect("/ingredients")


@app.route("/ingredients/remove", methods=["POST"])
def ingredients_remove():
    global response
    try:
        inv_tracker.remove_entry(request.form["id"])
        response = f"Success: Removed '{request.form['name']}'."
    except Exception as e:
        response = f"Error: Ingredient '{request.form['name']}' not found in database."
    return redirect("/ingredients")


@app.route("/recipes", methods=["GET"])
def recipes():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "
    recipe_recommender.get_recommendations(inv_tracker, 2)
    return render_template("recipes.html", recipes = recipe_recommender.recommendations, recipes_JSON = recipe_recommender.jsonify(inv_tracker), response=response)


@app.route("/recipes/search", methods=["POST"])
def recipes_search():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    return jsonify("{}")  # Return a JSON of results



@app.route("/shoppinglist", methods=["GET"])
def shoppinglist():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "
    
    return render_template("shoppinglist.html", shoppinglist=shop_list.shopping_list.values(), shoppinglist_JSON=shop_list.jsonify())


@app.route("/shoppinglist/add", methods=["POST"])
def add_shoppinglist():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    if request.method == "POST":
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        shop_list.add_item(name, quantity, unit)
    return redirect("/shoppinglist")


@app.route("/shoppinglist/modify", methods=["POST"])
def modify_shoppinglist():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    mod_id = request.form["id"]
    new_name = request.form["name"]
    new_quantity = float(request.form["quantity"])
    new_unit = request.form["unit"]
    shop_list.modify_item(mod_id, new_name, new_quantity, new_unit)
    return redirect("/shoppinglist")


@app.route("/shoppinglist/remove", methods=["POST"])
def remove_shoppinglist():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    
    return redirect("/shoppinglist")


@app.route("/shoppinglist/purchase", methods=["POST"])
def purchase_shoppinglist():
    global response
    try:
        
        response = "Success: "
    except Exception as e:
        
        response = "Error: "

    pur_id = request.form["id"]
    # TODO request expiration date from user when you hit the purchase button
    name = request.form['name']
    quantity = float(request.form['quantity'])
    unit = request.form['unit']
    exp_date = request.form['expiration_date']
    inv_tracker.add_entry(name, quantity, unit, exp_date)
    shop_list.remove_item(pur_id)
    return redirect("/shoppinglist")


app.run(debug = True)