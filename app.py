from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from random import choice, randint
from unittest import TestCase
import requests
import re
from sqlalchemy import desc
from flask_cors import CORS
from secrets import API_KEY
from flask_debugtoolbar import DebugToolbarExtension
from forms import ReviewForm, UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Post, Wine, Favorite
from results import AllAbove, RedWhiteRose

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

all_above = AllAbove()
red_white_rose = RedWhiteRose()


##############################################################################
# User signup/login/logout


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


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                bio=form.bio.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


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

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    do_logout()
    return redirect('/login')





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

# ===================================    RETURN JSON  =====================================

@app.route('/show_all_wines_json')
def return_all_wines_json():
    all_reds = [red.serialize() for red in Wine.query.all()]
    return jsonify(red_wines=all_reds)

@app.route('/show_all_white_json')
def return_white_wine_json():
    all_white = [white.serialize() for white in Wine.query.filter_by(type='White').all()]
    return jsonify(white_wines=all_white)

@app.route('/show_all_red_json')
def return_red_wine_json():
    all_red = [red.serialize() for red in Wine.query.filter_by(type='Red').all()]
    return jsonify(red_wines=all_red)

@app.route('/show_all_rose_json')
def return_all_rose_wine_json():
    all_rose = [rose.serialize() for rose in Wine.query.filter_by(type='Rose').all()]
    return jsonify(rose_wines=all_rose)

# ===================================    SHOW VARIETALS   =====================================


@app.route('/show_red_varietals')
def show_red_varietals():
    
    red_list = []
    varietal_set = set()
    session['varietals'] = ""
    session['type'] = ""
    session['type'] = "Red"
    
    all_options = [red.varietal.split(",") for red in Wine.query.filter_by(type='Red').all()]
    
    for options in all_options:
        red_list = red_list + options
    
    
    
    for item in red_list:
        has_number = re.search("\d", item)
        has_blend = re.search(" Blend", item)
        has_plus = re.search("\+", item)
        has_slash = re.search("/", item)
        has_period = re.search("\.", item)
        has_ampersand = re.search("&", item)
        if item != "" and not has_number and len(item) < 25 and not has_blend and not has_plus and not has_slash and not has_period and not has_ampersand:
            title_case_item = item.title()
            varietal_set.add(title_case_item.strip())
        
    return render_template("varietal_options.html", varietal_set=varietal_set)


@app.route('/show_white_varietals')
def show_white_varietals():
    
    white_list = []
    varietal_set = set()
    session['varietals'] = ""
    session['type'] = ""
    session['type'] = "White"
    
    all_options = [white.varietal.split(",") for white in Wine.query.filter_by(type='White').all()]
    
    for options in all_options:
        white_list = white_list + options
    
    for item in white_list:
        has_number = re.search("\d", item)
        has_blend = re.search(" Blend", item)
        has_plus = re.search("\+", item)
        has_slash = re.search("/", item)
        has_period = re.search("\.", item)
        has_ampersand = re.search("&", item)
        if item != "" and not has_number and len(item) < 25 and not has_blend and not has_plus and not has_slash and not has_period and not has_ampersand:
            title_case_item = item.title()
            varietal_set.add(title_case_item.strip())
        
    return render_template("varietal_options.html", varietal_set=varietal_set)


@app.route('/show_rose_varietals')
def show_rose_varietals():
    
    rose_list = []
    varietal_set = set()
    session['varietals'] = ""
    session['type'] = ""
    session['type'] = "Rose"
    
    all_options = [rose.varietal.split(",") for rose in Wine.query.filter_by(type='Rose').all()]
    
    for options in all_options:
        rose_list = rose_list + options
    
    for item in rose_list:
        has_number = re.search("\d", item)
        has_blend = re.search(" Blend", item)
        has_plus = re.search("\+", item)
        has_slash = re.search("/", item)
        has_period = re.search("\.", item)
        has_ampersand = re.search("&", item)
        if item != "" and not has_number and len(item) < 25 and not has_blend and not has_plus and not has_slash and not has_period and not has_ampersand:
            title_case_item = item.title()
            varietal_set.add(title_case_item.strip())
        
    return render_template("varietal_options.html", varietal_set=varietal_set)

# ===================================    WINE RESULTS   =====================================

@app.route('/show_combined_question/<new_varietal>')
def get_varietal_choices(new_varietal):

    if session['varietals']:
        varietals = session['varietals']
    else:
        varietals = []

    if new_varietal in varietals:

        index = varietals.index(new_varietal)
        varietals.pop(index)
    else:
        varietals.append(new_varietal)

    session['varietals'] = [wine for wine in varietals]

    return render_template("combined_only.html", varietals=varietals)
  

@app.route('/show_combined_question')
def show_combined_question():

    varietals = session['varietals']
    
    if varietals == "" or varietals is None:
        return redirect("/show_all_wine")
    
    if len(varietals) == 1:
        multiple_varietals = False
        return render_template("combined_only.html", multiple_varietals=multiple_varietals)
    else:
        multiple_varietals = True   
  
    return render_template("combined_only.html", multiple_varietals=multiple_varietals)

@app.route('/show_all_wine')
def show_all_wine_results():
    
    varietals = session['varietals']
    
    if varietals == "" or varietals is None:
        all_wine = Wine.query.order_by(desc(Wine.rating)).all()

    return render_template("wine_results.html", wines=all_wine)

@app.route('/show_exact_results')
def show_exact_wine_results():
    
    varietals = session['varietals']
    wine_type = session['type']
    exact_matches = []
    
    if len(varietals) == 1:
        varietal = varietals[0]
        wines = Wine.query.filter_by(type=wine_type).all()
        for wine in wines:
            varietal_description = wine.varietal
            if re.search(r"^" + varietal + r"$", varietal_description):
                exact_matches.append(wine)
                
    else:
        wines = Wine.query.filter_by(type=wine_type).all()
        for wine in wines:
            if all(x in wine.varietal for x in varietals):
                exact_matches.append(wine)
        
            
                
    return render_template("wine_results.html", wines=exact_matches)


@app.route('/show_close_to_results')
def show_wine_results():
    
    varietals = session['varietals']
    wine_type = session['type']
    all_wine = []
    
    for varietal in varietals:
        results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).all()
  
        for result in results:
            all_wine.append(result)
    
    return render_template("wine_results.html", wines=all_wine)

# ===================================    HOME    =====================================


@app.route('/')
def homepage():
    """Show homepage"""
    session['wine_type'] = ""
    session['varietals'] = []
    session['filters'] = ['Red', 'White', 'Rose', 'All of the above', 'Rating (Highest)', 'Rating (Lowest)', 'Vintage (Oldest)', 'Vintage (Youngest)', 'Winery (Alphabetically)']
    
    
    
    return render_template("new_home.html")


# ===================================    ADDING PARAMETERS TO SESSION   =====================================

@app.route('/wine_type/<new_wine_type>')
def get_wine_type_choices(new_wine_type):

    # wine_type = []

    # wine_type.append(new_wine_type)

    session['wine_type'] = new_wine_type
    

    return render_template("new_home.html")

@app.route('/wine_style/<new_wine_style>')
def get_wine_style_choices(new_wine_style):

    # wine_style = []

    # wine_style.append(new_wine_style)

    session['wine_style'] = new_wine_style
    
    # import pdb
    # pdb.set_trace()

    return render_template("new_home.html")


@app.route('/sort_by/<new_sort_by>')
def get_sort_by_choices(new_sort_by):

    # sort_by = []

    # sort_by.append(new_sort_by)

    session['sort_by'] = new_sort_by
    
    # import pdb
    # pdb.set_trace()

    return render_template("new_home.html")

# ===================================    ADDING VARIETALS TO SESSION   =====================================

@app.route('/get_varietals')
def get_varietals():

    wine_list = []
    varietal_set = set()
    if session['varietals']:
        selected_varietals = session['varietals']
    else:
        selected_varietals = []


    
    if session['wine_type'] != "":
        wine_type = session['wine_type']
    else:
        wine_type = "All of the above"

    if wine_type == "All of the above":
        all_options = [wine.varietal.split(",") for wine in Wine.query.all()]

    else:    
        all_options = [wine.varietal.split(",") for wine in Wine.query.filter_by(type=wine_type).all()]
    
    for options in all_options:
        wine_list = wine_list + options
    
    
    
    for item in wine_list:
        has_number = re.search("\d", item)
        has_blend = re.search(" Blend", item)
        has_plus = re.search("\+", item)
        has_slash = re.search("/", item)
        has_period = re.search("\.", item)
        has_ampersand = re.search("&", item)
        if item != "" and not has_number and len(item) < 25 and not has_blend and not has_plus and not has_slash and not has_period and not has_ampersand:
            title_case_item = item.title()
            varietal_set.add(title_case_item.strip())
            
    # import pdb
    # pdb.set_trace()
    # session['varietals'] = varietal_set
    varietals = [varietal for varietal in varietal_set]

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
    
   

    return render_template("combined_only.html", varietals=varietals)

# ===================================    SHOWING RESULTS   =====================================

@app.route('/show_results')
def show_results():
    
    varietals = session['varietals']
    wine_type = session['wine_type']
    wine_style = session['wine_style']
    sort_by = session['sort_by']

    if wine_type == 'All of the above':
        if wine_style == 'Single Varietals Only':
            wine_results = all_above.single_varietal(sort_by, varietals)
        else:
            wine_results = all_above.blends(sort_by, varietals)
    else:
        if wine_style == 'Single Varietals Only': 
            wine_results = red_white_rose.single_varietal(wine_type, sort_by, varietals)
        else:
            wine_results = red_white_rose.blends(wine_type, sort_by, varietals)
                
    return render_template("wine_results.html", wines=wine_results)


# ===================================    ADDING RESULTS PAGE FILTERS TO SESION   =====================================


@app.route('/log_filters/<new_filter>')
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
    
   

    return render_template("combined_only.html", varietals=varietals)