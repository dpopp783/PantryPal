from flask import *

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/shoppinglist")
def shoppinglist():
    return render_template("shoppinglist.html")