from flask import *
from data_util import *
import config

from inventory_tracker import InventoryTracker
from inventory_entry import InventoryEntry, Ingredient, PantryPalIngredientIDMap
from shopping_list import ShoppingList
from recipe_recommender import Recipe, RecipeRecommender
import datetime
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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
app.secret_key = config.api_key # This just has to exist to use sessions


@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form["username"]
        password = request.form["password"]
        
        with open("accounts.json", "r") as f:
            accounts: dict = json.load(f)
            if not accounts.get(username, None):
                raise Exception(f"Could not find account '{username}'.")
            elif accounts.get(username) != password:
                raise Exception(f"Incorrect password for '{username}'.")
            else:
                session["username"] = username

        flash(f"Logged in as '{username}'", "success")
        return redirect("/dashboard")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/")
    

@app.route("/signup", methods=["POST"])
def signup():
    try:
        username = request.form["username"]
        password = request.form["password"]
        with open("accounts.json", "r") as f:
            accounts: dict = json.load(f)
            if accounts.get(username, None):
                raise Exception(f"Account '{username}' already exists.")
            elif not password:
                raise Exception(f"Password must be one or more characters.")
            else:
                accounts[username] = password

        with open("accounts.json", "w") as f:
            json.dump(accounts, f, indent=4)
        
        session["username"] = username
        flash(f"Successfully created account '{username}'")
        return redirect("/dashboard")
    
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if session.get("username", None):
        try:
            inventory = InventoryTracker(session["username"])
            shoppinglist = ShoppingList(session["username"])
            recommender = RecipeRecommender()
            recipe = recommender.get_recommendations(inventory, 1)[0]
            return render_template("dashboard.html", 
                user = session["username"],
                inventory = inventory.to_dict(), 
                shoppinglist = shoppinglist.to_dict(),
                recipe = recipe.to_dict(inventory),
            )
        
        except Exception as e:
            print(e)
            flash(str(e), "danger")
        
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/ingredients", methods=["GET"])
def ingredients():
    if session.get("username", None):
        try:
            inv = InventoryTracker(session["username"])
            return render_template("ingredients.html", inventory=inv.inventory, inventory_JSON=inv.jsonify())
        
        except Exception as e:
            flash(str(e), "danger")
            return render_template("ingredients.html", inventory={}, inventory_JSON={})
        
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/ingredients/add", methods=["POST"])
def ingredients_add():
    if session.get("username", None):
        try:
            name = request.form['name']
            quantity = float(request.form['quantity'])
            unit = request.form['unit']
            exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()

            inv = InventoryTracker(session["username"])   
            inv.add_entry(name, quantity, unit, exp_date)
            save_data(session["username"], inv.to_dict(), "inventory")
            flash(f"Successfully added entry '{name}'")

        except Exception as e:
            flash(str(e), "danger")

        return redirect("/ingredients")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/ingredients/modify", methods=["POST"])
def ingredients_modify():
    if session.get("username", None):
        try:
            print(request.form)
            mod_id = request.form["id"]
            new_name = request.form["name"]
            new_quantity = float(request.form["quantity"])
            new_unit = request.form["unit"]
            if len(request.form['expiration_date']):
                new_exp_date = datetime.datetime.strptime(request.form['expiration_date'], '%Y-%m-%d').date()
            else:
                new_exp_date = None

            inv = InventoryTracker(session["username"])
            inv.modify_entry(mod_id, new_name, new_quantity, new_unit, new_exp_date)
            save_data(session["username"], inv.to_dict(), "inventory")
            flash(f"Successfully updated entry '{new_name}'", "success")

        except Exception as e:
            print(e)
            flash(str(e), "danger")

        return redirect("/ingredients")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/ingredients/remove", methods=["POST"])
def ingredients_remove():
    if session.get("username", None):
        try:
            inv = InventoryTracker(session["username"])
            inv.remove_entry(request.form["id"])
            save_data(session["username"], inv.to_dict(), "inventory")
            flash(f"Successfully deleted entry '{request.form['name']}'")

        except Exception as e:
            flash(str(e), "error")

        return redirect("/ingredients")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/recipes", methods=["GET"])
def recipes():
    if session.get("username", None):
        try:
            inventory = InventoryTracker(session["username"])
            recommender = RecipeRecommender()
            recipes = recommender.get_recommendations(inventory, 20)
            return render_template("recipes.html", recipes = recipes, recipes_JSON = recommender.jsonify(inventory))
        
        except Exception as e:
            flash(str(e), "danger")
            return render_template("recipes.html", recipes = {}, recipes_JSON = {})
        
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/recipes/search", methods=["POST"])
def recipes_search():
    if session.get("username", None):
        try:
            pass
        except Exception as e:
            flash(str(e), "danger")

        return jsonify("{}")  # Return a JSON of results
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/recipes/buy-ingredients", methods=["POST"])
def recipes_buy_ingredients():
    if session.get("username", None):
        try:
            recipe = request.get_json()
            ingredients = recipe['missedIngredients']
            shoppinglist = ShoppingList(session["username"])

            for ingredient in ingredients:
                shoppinglist.add_item(ingredient["ingredient"]["name"], ingredient["quantity"], ingredient["unit"])

            save_data(session["username"], shoppinglist.to_dict(), "shoppinglist")
            flash(f"Added missing ingredients of '{recipe['name']}' to your Shopping List", "success")

        except Exception as e:
            flash(str(e), "danger")

        return redirect("/recipes")

    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/shoppinglist", methods=["GET"])
def shoppinglist():
    if session.get("username", None):
        try:
            
            shop = ShoppingList(session["username"])
            return render_template("shoppinglist.html", shoppinglist=shop.to_dict(), shoppinglist_JSON=shop.jsonify())
        
        except Exception as e:
            flash(str(e), "danger")
        return render_template("shoppinglist.html", shoppinglist={}, shoppinglist_JSON={})
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/shoppinglist/add", methods=["POST"])
def add_shoppinglist():
    if session.get("username", None):
        try:
            pass
        except Exception as e:
            flash(str(e), "danger")

        if request.method == "POST":
            name = request.form['name']
            quantity = float(request.form['quantity'])
            unit = request.form['unit']
            shop_list.add_item(name, quantity, unit)
        return redirect("/shoppinglist")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/shoppinglist/modify", methods=["POST"])
def modify_shoppinglist():
    if session.get("username", None):
        try:  
            pass
        except Exception as e:
            flash(str(e), "danger")

        mod_id = request.form["id"]
        new_name = request.form["name"]
        new_quantity = float(request.form["quantity"])
        new_unit = request.form["unit"]
        shop_list.modify_item(mod_id, new_name, new_quantity, new_unit)
        return redirect("/shoppinglist")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/shoppinglist/remove", methods=["POST"])
def remove_shoppinglist():
    if session.get("username", None):
        try:
            pass
        except Exception as e:
            flash(str(e), "danger")

        return redirect("/shoppinglist")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


@app.route("/shoppinglist/purchase", methods=["POST"])
def purchase_shoppinglist():
    if session.get("username", None):
        try:
            pass
        except Exception as e:
            flash(str(e), "danger")

        pur_id = request.form["id"]
        name = request.form['name']
        quantity = float(request.form['quantity'])
        unit = request.form['unit']
        exp_date = request.form['expiration_date']
        inv_tracker.add_entry(name, quantity, unit, exp_date)
        shop_list.remove_item(pur_id)
        return redirect("/shoppinglist")
    else:
        flash("Please log in to use PantryPal", "danger")
        return redirect("/")


app.run(debug = True)