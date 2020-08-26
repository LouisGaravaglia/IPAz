from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from random import choice, randint
from unittest import TestCase
import requests
import re
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from secrets import API_KEY
from flask_debugtoolbar import DebugToolbarExtension
from forms import ReviewForm, UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Post, Wine, Favorite
from results import WineResults
from get_varietals import Varietals

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wine_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
# app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

connect_db(app)

debug = DebugToolbarExtension(app)

filter_results = WineResults()
varietal_cls = Varietals()


# ===================================    USER VALIDATING FUNCTIONS    =====================================



@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None
        

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# ===================================    SIGN UP    =====================================


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()
    
    # if form.is_submitted():
    #     print("submitted")
    

    # if form.validate():
    #     print("valid")
        
    # print(form.errors)

    if form.validate_on_submit():
        
        try:
            user = User.signup(
                name=form.name.data,
                username=form.username.data,
                password=form.password.data
                # bio=form.bio.data,
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

# ===================================    LOGIN    =====================================

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

# ===================================    LOGOUT    =====================================


@app.route('/logout')
def logout():
    do_logout()
    return redirect('/login')

# ===================================    PROFILE ROUTE   =====================================

@app.route('/user')
def profile_page():
    """Show profile page"""

    # import pdb
    # pdb.set_trace()
    
    user_id = session[CURR_USER_KEY]
    
    user = User.query.get_or_404(user_id)
    
    return render_template("profile.html", user=user)


# ===================================    FAVORITES ROUTE    =====================================

@app.route("/user/add_like/<int:wine_id>", methods=['POST'])
def add_like(wine_id):
    """Add the liked message user id to a list."""
    
    # import pdb
    # pdb.set_trace()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/show_results")

    faved_wine = Wine.query.get_or_404(wine_id)
    # if faved_wine.user_id in g.user.fav_wines:
    #     flash("You've already liked that.", "danger")
    #     return redirect("/")
    
    user_favorites = g.user.fav_wines
    
    if faved_wine in user_favorites:
        g.user.fav_wines = [wine for wine in user_favorites if wine != faved_wine]
    else:
        g.user.fav_wines.append(faved_wine)
        
    db.session.commit()

    return redirect("/show_results")

# ===================================    REVIEWS ROUTE    =====================================



##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

# ===================================    PICK TYPE OF WINE    =====================================


@app.route('/wine_types')
def show_wine_types():
    """Show options for wine types to choose from"""
    
    return render_template("wine_types.html")

# ===================================    API CALLS    =====================================

@app.route('/api/get_red_wines')
def get_red_wines():
    """Get all top rated red wines from the API"""  
    
    baseURL = "https://quiniwine.com/api/pub/wineCategory/tre/0/1000"
    headers = {'authorization': API_KEY}
    
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    
    if result.status_code != 200:
       return jsonify(message="There was an issue making an request for red wines to the API.") 
   

    for wine in wine_array:
        new_wine = Wine(
            wine_id = wine["_id"],
            winery = wine["Winery"],
            country = wine["Country"],
            area = wine["Area"],
            vintage = wine["vintage"],
            varietal = wine["Varietal"],
            type = wine["Type"],
            name = wine["Name"],
            rating = wine["rating"]
        )
        
        db.session.add(new_wine)
        db.session.commit()
 
    return jsonify(message="Successful request. All red wines imported into database.")


@app.route('/api/get_white_wines')
def get_white_wines():
    """Get all top rated white wines from the API"""  

    baseURL = "https://quiniwine.com/api/pub/wineCategory/twh/0/1000"
    headers = {'authorization': API_KEY}
    
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    
    if result.status_code != 200:
       return jsonify(message="There was an issue making an request for white wines to the API.") 

    for wine in wine_array:
        new_wine = Wine(
            wine_id = wine["_id"],
            winery = wine["Winery"],
            country = wine["Country"],
            area = wine["Area"],
            vintage = wine["vintage"],
            varietal = wine["Varietal"],
            type = wine["Type"],
            name = wine["Name"],
            rating = wine["rating"]
        )
        
        db.session.add(new_wine)
        db.session.commit()
 
    return jsonify(message="Successful request. All white wines imported into database.")


@app.route('/api/get_rose_wines')
def get_rose_wines():
    """Get all top rated rose wines from the API"""  

    baseURL = "https://quiniwine.com/api/pub/wineCategory/tro/0/1000"
    headers = {'authorization': API_KEY}
    
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    
    # import pdb
    # pdb.set_trace()
    if result.status_code != 200:
       return jsonify(message="There was an issue making an request for rose wines to the API.") 
    

    for wine in wine_array:
        new_wine = Wine(
            wine_id = wine["_id"],
            winery = wine["Winery"],
            country = wine["Country"],
            area = wine["Area"],
            vintage = wine["vintage"],
            varietal = wine["Varietal"],
            type = wine["Type"],
            name = wine["Name"],
            rating = wine["rating"]
        )
        
        db.session.add(new_wine)
        db.session.commit()
 
    return jsonify(message="Successful request. All rose wines imported into database.")


# ===================================    HOME    =====================================


@app.route('/')
def homepage():
    """Show homepage"""
    session['varietals'] = []
    session['filters'] = ['Red', 'White', 'Rose', 'All of the above', 'Rating (Highest)', 'Rating (Lowest)', 'Vintage (Oldest)', 'Vintage (Youngest)', 'Winery (Alphabetically)']
    session['filter_by'] = []
    session['wine_style'] = "All"
    
    all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]

    varietals = varietal_cls.get_all_varietals(all_varietals)
    # import pdb
    # pdb.set_trace()
    
    return render_template("new_home.html", varietals=varietals)


# ===================================    ADDING PARAMETERS TO SESSION   =====================================

@app.route('/wine_type/<new_wine_type>')
def get_wine_type_choices(new_wine_type):
    
    filter_list = session['filter_by']
    
    if (new_wine_type == 'Red' or new_wine_type == 'White' or new_wine_type == 'Rose') and 'All of the above' in filter_list:
        filter_list.remove('All of the above')
    
    if new_wine_type in filter_list:
        filter_list.remove(new_wine_type)
    else:    
        filter_list.append(new_wine_type)
        
    session['filter_by'] = filter_list

    # import pdb
    # pdb.set_trace()
    
    return render_template("new_home.html")

@app.route('/wine_style/<new_wine_style>')
def get_wine_style_choices(new_wine_style):

    varietals = session['varietals']
    filter_list = session['filter_by']
    
    # import pdb
    # pdb.set_trace()
    
    if new_wine_style != '""':
        session['wine_style'] = new_wine_style
    else:
        new_wine_style = session['wine_style']
    
    if new_wine_style == 'All':
        wine_results = filter_results.all_wines(filter_list, varietals)
    elif new_wine_style == 'Blends Only':
        wine_results = filter_results.blends_only(filter_list, varietals)
    else: 
        wine_results = filter_results.single_varietal(filter_list, varietals)
        
    if wine_results == []:
        wine_results = ['No Results']
    
    
        
    if g.user:
        user_favorites = []
        user_favs = g.user.fav_wines
        for fav in user_favs:
            user_favorites.append(fav.id)
        
    else:
        user_favorites = []
        
    

    
    
    return jsonify(wine_results=wine_results, user_favorites=user_favorites)



@app.route('/sort_by/<new_sort_by>')
def get_sort_by_choices(new_sort_by):

    filter_list = session['filter_by']
    
    if new_sort_by in filter_list:
        filter_list.remove(new_sort_by)
    else:    
        filter_list.append(new_sort_by)
        
    session['filter_by'] = filter_list

    
    # import pdb
    # pdb.set_trace()

    return render_template("new_home.html")

# ===================================    ADDING VARIETALS TO SESSION   =====================================

@app.route('/get_varietals')
def get_varietals():

    varietal_list = []
    red_varietals = []
    white_varietals = []
    rose_varietals = []
    all_varietals = []
    varietal_set = set()
    
    if session['varietals']:
        selected_varietals = session['varietals']
    else:
        selected_varietals = []


    filter_list = session['filter_by']
    
    # import pdb
    # pdb.set_trace()
    
    if 'Red' in filter_list:
        red_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        
    if 'White' in filter_list:
        white_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        
    if 'Rose' in filter_list:
        rose_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
        
    if not 'Red' in filter_list and not 'White' in filter_list and not 'Rose' in filter_list or 'All of the above' in filter_list:
        all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]
        
    merged_varietals = red_varietals + white_varietals + rose_varietals + all_varietals
    
    varietals = varietal_cls.get_all_varietals(merged_varietals)
    

    return jsonify(varietals=varietals, selected_varietals=selected_varietals)

    
    
@app.route('/log_varietals/<new_varietal>')
def log_varietal_choice(new_varietal):

    if session['varietals']:
        varietals = session['varietals']
    else:
        varietals = []

    # import pdb
    # pdb.set_trace()
    
    if new_varietal in varietals:

        index = varietals.index(new_varietal)
        varietals.pop(index)
    else:
        varietals.append(new_varietal)

    session['varietals'] = [wine for wine in varietals]
    
    return jsonify(varietals=varietals)



# ===================================    SHOWING RESULTS   =====================================

@app.route('/show_results')
def show_results():
    
    varietals = session['varietals']
    filter_list = session['filter_by']

   
    wine_results = filter_results.all_wines(filter_list, varietals)
    
    if g.user:
        user_favorites = []
        user_favs = g.user.fav_wines
        for fav in user_favs:
            user_favorites.append(fav.id)
        
    else:
        user_favorites = []
    
    if wine_results == []:
        wine_results = ['No Results']

    return render_template("wine_results.html", wines=wine_results, user_favorites=user_favorites)

