import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, flash, get_flashed_messages
import pymongo
import bcrypt 
from routes import login_required, find
import json 

load_dotenv() 
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


client = pymongo.MongoClient(f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@travel-app.kfdzca6.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('users')
users = db.authentication

#Create category dictionary, mapping its aliases to titles. 
category_file = open("restaurant-categories.json")
categories = json.load(category_file)
category_dict = {}
for category in categories:
    title = category.get('title')
    alias = category.get('alias')
    category_dict[title] = alias    

@app.route('/')
def index(): 
    if 'username' in session:
        return render_template("index.html", message=session["username"])
    return redirect("/login")

@app.route('/login', methods=["GET", "POST"])
def login():
    flashed_msg = ''
    if request.method == "POST":
        login_user = users.find_one({'name' : request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode("utf-8"), login_user['password']) == login_user["password"]:
                session["username"] = request.form["username"]
                return redirect('/')
            flash('Invalid password. Please try again.')
        else:
            flash('Invalid username. Please try again.')
        flashed_msg = get_flashed_messages()[0]
    return render_template("/login.html", flashed_msg=flashed_msg)

@app.route('/register', methods=["GET", "POST"])
def register():
    flashed_msg = ''
    if request.method == "POST":
        existing_user = users.find_one({'name': request.form['username']})
        if existing_user is None:
            hashed = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())
            users.insert_one({'name': request.form["username"], 'password': hashed, 'wishlist': [], 'favorites': []})
            return redirect(url_for('login'))
        flash('A user already exists with that username.', 'error')
        flashed_msg = get_flashed_messages()[0]
    return render_template("/register.html", flashed_msg=flashed_msg)

def parse_req(input):
    input = input.split("✘ ")
    keys = ["name", "rating", "price", "category", "website", "image", "address"]
    new_item = dict(zip(keys, input))
    return new_item

def act(item, add_to, action):
    new_item = parse_req(item)
    users.find_one_and_update({'name': session['username']}, {action: {add_to: new_item}})
    return new_item 

@app.route('/wishlist', methods=["GET", "POST"])
@login_required
def wishlist():
    wishlist_array = users.find_one({'name' : session['username']})['wishlist']
    if request.method == "POST" and len(wishlist_array) < 4:
        added = request.form['added']
        item = act(added, 'wishlist', '$addToSet')
        wishlist_array.append(item)
    return render_template('/wishlist.html', wishlist_array=wishlist_array)

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    #idea: change categories to be a scrollable dropdown select menu
    if request.method == "POST":
        location = request.form.get("location")
        categories = request.form.get("categories")
        categories = category_dict[categories]
        price = request.form.get("price") 
        p_range = range(1, int(price) + 1)
        p_range = [str(i) for i in p_range]
        price_range = ", ".join(p_range)
        results = find(location, categories, price_range)
        return render_template("/search_results.html", location=location, categories=categories, results=results)
    return render_template('/search.html', categories=category_dict.keys())

@app.route('/remove_wish', methods=["GET", "POST"])
@login_required
def remove_wishlist():
    if request.method == "POST": 
        removed = request.form['removed']
        act(removed, 'wishlist', '$pull')
    return redirect('/wishlist')

@app.route('/remove_fav', methods=["GET", "POST"])
@login_required
def remove_fav():
    if request.method == "POST": 
        removed = request.form['removed']
        act(removed, 'favorites', '$pull')
    return redirect('/favorite')

@app.route('/favorite', methods=["GET", "POST"])
@login_required
def favorite():
    favorites_array = users.find_one({'name' : session['username']})['favorites']
    fav_count = len(favorites_array)
    if request.method == "POST" and fav_count < 8:
        liked = request.form['liked']
        new_item = act(liked, 'favorites', '$addToSet')
        fav_count += 1
        favorites_array.append(new_item)
    return render_template('/favorites.html', favorites=favorites_array)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("/login.html")

if __name__ == "__main__":
    app.run(debug=True)