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
from forms import ReviewForm, UserAddForm, LoginForm, UserEditForm, EditReviewForm, EditUserForm
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

get_wine = WineResults()
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

        flash("Invalid credentials.", 'error')

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

    if not g.user:
        flash("Please log in or sign up!", "error")
        return redirect("/show_results")
    
    user_id = session[CURR_USER_KEY]
    
    user = User.query.get_or_404(user_id)
    
    if g.user.posts and g.user.fav_wines:
        reviews = g.user.posts
        num_of_reviews = len(reviews)
            
        top_rated_review = Post.query.order_by(Post.rating.desc()).first()
        top_rated_wine = Wine.query.get_or_404(top_rated_review.wine_id)

        likes = g.user.fav_wines
        num_of_favs = len(likes)
        
        most_recent = Favorite.query.filter(Favorite.user_id == user_id).order_by(Favorite.id.desc()).first()
        most_recent_fav = Wine.query.get_or_404(most_recent.wine_id)
        
        return render_template("profile.html", user=user, num_of_favs=num_of_favs, num_of_reviews=num_of_reviews, top_rated_review=top_rated_review, top_rated_wine=top_rated_wine, most_recent_fav=most_recent_fav)

        
    elif g.user.posts:
        reviews = g.user.posts
        num_of_reviews = len(reviews)
        
        top_rated_review = Post.query.order_by(Post.rating.desc()).first()
        top_rated_wine = Wine.query.get_or_404(top_rated_review.wine_id)
        
        return render_template("profile.html", user=user, num_of_reviews=num_of_reviews, top_rated_review=top_rated_review, top_rated_wine=top_rated_wine)

    
    elif g.user.fav_wines:
        likes = g.user.fav_wines
        num_of_favs = len(likes)
        
        most_recent = Favorite.query.filter(Favorite.user_id == user_id).order_by(Favorite.id.desc()).first()
        most_recent_fav = Wine.query.get_or_404(most_recent.wine_id)
        
        return render_template("profile.html", user=user, num_of_favs=num_of_favs, most_recent_fav=most_recent_fav)

    
    else:
    
        return render_template("profile.html", user=user)

    
   

        
    


# ===================================    EDIT PROFILE ROUTE   =====================================

@app.route('/user/edit/<int:user_id>', methods=["GET", "POST"])
def edit_profile_page(user_id):
    """Show profile page"""

    
    
    if not g.user:
        flash("Please log in or sign up to edit your profile!", "error")
        return redirect("/show_results")
    
    form = EditUserForm()
    


    if form.validate_on_submit():
        # import pdb
        # pdb.set_trace()
     
        user = User.query.get_or_404(user_id)
    
        user.name = form.name.data
        user.username = form.username.data
        
        db.session.commit()

    
        return redirect("/user")

    else:
  
    
        return render_template('edit_profile.html', form=form)



# ===================================    ADDING FAVORITE   =====================================

@app.route("/user/add_favorite/<int:wine_id>", methods=['POST'])
def add_like(wine_id):
    """Add the liked message user id to a list."""
    
    # import pdb
    # pdb.set_trace()

    if not g.user:
        # flash("Please log in or sign up to favorite wine!", "error")
        return jsonify(message="Please log in or sign up to favorite wines!") 



        
    faved_wine = Wine.query.get_or_404(wine_id)


    if faved_wine in g.user.fav_wines:
        g.user.fav_wines = [wine for wine in g.user.fav_wines if wine != faved_wine]
    else:
        g.user.fav_wines.append(faved_wine)
        
    db.session.commit()
    
    fav_ids = []
    fav_wines = []
    wine_reviews = []

    
    for wine in g.user.fav_wines:
        fav_ids.append(wine.id)
        fav_wines.append({'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name})
    
    for review in g.user.posts:
        wine = Wine.query.get_or_404(review.wine_id)
        post = {'Post_id':review.id, 'Post_rating':review.rating, 'Post_review':review.review, 'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name}                  
        wine_reviews.append(post)
        
    # import pdb
    # pdb.set_trace()

    return jsonify(fav_wine_list=fav_ids, fav_wines=fav_wines, wine_reviews=wine_reviews)

# ===================================    VIEWING FAVORITES   =====================================

@app.route("/user/favorites")
def view_favorites():
    """Viewing all favorited wines of the user."""
    
    # import pdb
    # pdb.set_trace()

    if not g.user:
        flash("Access unauthorized.", "error")
        return redirect("/show_results")

    # user = User.query.get_or_404(g.user.id)
    faved_wines = g.user.fav_wines
    
   
    user_reviews = []
    for post in g.user.posts:
        user_reviews.append(post.wine_id)
    
    # if faved_wine.user_id in g.user.fav_wines:
    #     flash("You've already liked that.", "danger")
    #     return redirect("/")
    


    return render_template("favorites.html", faved_wines=faved_wines, user_reviews=user_reviews)

# ===================================    SINGLE REVIEW / POST    =====================================

@app.route('/user/review/<int:wine_id>', methods=['GET', 'POST'])
def review(wine_id):
    """Handle going to review form for a specific wine, 
    and posting the review.
    """
    
    if not g.user:
        flash("Please log in or sign up to review wines!", "error")
        return redirect("/show_results")
    
    user_reviews = []
    for post in g.user.posts:
        user_reviews.append(post.wine_id)
    
     
    if wine_id in user_reviews:
        flash("This wine has already been reivewed.", "error")
        return redirect("/user/reviews")
    
  
    form = ReviewForm()
    

    if form.validate_on_submit():
        
        rating = form.rating.data
        content = form.review.data
            
        review = Post(rating=rating, review=content, wine_id=wine_id, user_id=g.user.id)
        db.session.add(review)
        db.session.commit()

    
        return redirect("/user/reviews")

    else:
        
        wine = Wine.query.get_or_404(wine_id)
        
        # import pdb
        # pdb.set_trace()
        
        return render_template('review.html', form=form, wine=wine)

# ===================================    REVIEWS / GET   =====================================

@app.route('/user/reviews')
def view_reviews():
    """Handle going to review form for a specific wine, 
    and posting the review.
    """

    # if not g.user:
    #     return jsonify(message="Please log in or sign up to review wines!") 
    if not g.user:
        flash("Please log in or sign up to see your reviews!", "error")
        return redirect("/show_results")
    
    wine_reviews = []
    
    reviews = g.user.posts
    
    for review in reviews:
        wine = Wine.query.get_or_404(review.wine_id)
        post = {'Post_id':review.id, 'Post_rating':review.rating, 'Post_review':review.review, 'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name}                  
        wine_reviews.append(post)
    
  
    user_favorites = []
    user_favs = g.user.fav_wines
    for fav in user_favs:
        user_favorites.append(fav.id) 
 
    
    return render_template('view_reviews.html', wine_reviews=wine_reviews, user_favorites=user_favorites)


# ===================================    REVIEWS / PATCH   =====================================

@app.route('/user/reviews/<int:wine_id>', methods=["GET", "POST"])
def patch_reviews(wine_id):
    """Handle going to review form for a specific wine, 
    and posting the review.
    """

    if not g.user:
        flash("Please log in or sign up to see your reviews!", "error")
        return redirect("/show_results")
    
    form = EditReviewForm()
    


    if form.validate_on_submit():
        
     
        post = Post.query.filter(Post.wine_id == wine_id).first()
    
        post.rating = form.rating.data
        post.review = form.review.data
        
        db.session.commit()

    
        return redirect("/user/reviews")

    else:
  
        review = Post.query.filter(Post.wine_id == wine_id).first()
        wine = Wine.query.get_or_404(wine_id)
        original_post = {'Post_id':review.id, 'Post_rating':review.rating, 'Post_review':review.review, 'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name}                  
    
        return render_template('edit_review.html', form=form, original_post=original_post)


# ===================================    REVIEWS / DELETE   =====================================

@app.route('/user/reviews/<int:wine_id>/delete')
def delete_review(wine_id):
    """Handle going to review form for a specific wine, 
    and posting the review.
    """


    if not g.user:
        flash("Please log in or sign up to see your reviews!", "error")
        return redirect("/show_results")
 
    post = Post.query.filter(Post.wine_id == wine_id).first()

    db.session.delete(post)
    db.session.commit()
    
    
    fav_ids = []
    fav_wines = []
    wine_reviews = []

    
    for wine in g.user.fav_wines:
        fav_ids.append(wine.id)
        fav_wines.append({'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name})
    
    for review in g.user.posts:
        wine = Wine.query.get_or_404(review.wine_id)
        post = {'Post_id':review.id, 'Post_rating':review.rating, 'Post_review':review.review, 'ID':wine.id, 'Rating':wine.rating, 'Winery':wine.winery, 'Country':wine.country, 'Vintage':wine.vintage, 'Area':wine.area, 'Varietal':wine.varietal, 'Type':wine.type, 'Name':wine.name}                  
        wine_reviews.append(post)

    return jsonify(fav_ids=fav_ids, fav_wines=fav_wines, wine_reviews=wine_reviews)


    
# ===================================    CACHE    =====================================
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


# @app.route('/wine_types')
# def show_wine_types():
#     """Show options for wine types to choose from"""
    
#     return render_template("wine_types.html")

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
    session['varietals'] = ['All']
    session['filters'] = ['Red', 'White', 'Rose', 'All of the above', 'Rating (Highest)', 'Rating (Lowest)', 'Vintage (Oldest)', 'Vintage (Youngest)', 'Winery (Alphabetically)']
    session['sort_by'] = ['None']
    session['wine_type'] = ['All of the above']
    session['wine_style'] = ['All']
    session['wine_type_options'] = ['Red', 'White', 'Rose']
    session['wine_style_options'] = ['Blends', 'Single Varietals']
    session['sort_by_options'] = ['Rating (Highest)', 'Rating (Lowest)', 'Vintage (Oldest)', 'Vintage (Youngest)', 'Winery (Alphabetically)']
    # session['wine_results'] = ['None']
    
    all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]

    varietals = varietal_cls.get_all_varietals(all_varietals)
    # import pdb
    # pdb.set_trace()
    
    return render_template("new_home.html", varietals=varietals)


# ===================================    RECEIVING WINE TYPE PICKS   =====================================

@app.route('/wine_type/<new_wine_type>')
def get_wine_type_choices(new_wine_type):
    
    # import pdb
    # pdb.set_trace()
    
    wine_type = session['wine_type']
    
    if (new_wine_type == 'Red' or new_wine_type == 'White' or new_wine_type == 'Rose') and 'All of the above' in wine_type:
        wine_type.remove('All of the above')
    
    if new_wine_type in wine_type:
        wine_type.remove(new_wine_type)
    else:    
        wine_type.append(new_wine_type)
    
    if not len(wine_type):
        wine_type = ['All of the above']
        
    session['wine_type'] = wine_type

    
    
    return render_template("new_home.html")

# ===================================    RECEIVING WINE STYLE PICKS   =====================================

@app.route('/wine_style/<new_wine_style>')
def get_wine_style_choices(new_wine_style):

    varietals = session['varietals']
    sort_by = session['sort_by']
    wine_type = session['wine_type']
    wine_style = session['wine_style']
    
    # import pdb
    # pdb.set_trace()

    if new_wine_style == '""':
       new_wine_style = session['wine_style'] 
        
    else:
        if (new_wine_style == 'Blends' or new_wine_style == 'Single Varietals') and 'All' in wine_style:
            wine_style.remove('All')
        
        if new_wine_style in wine_style:
            wine_style.remove(new_wine_style)
        else:    
            wine_style.append(new_wine_style)
        
        if len(wine_style) == 0:
            wine_style = ['All']
        
    session['wine_style'] = wine_style    

    wine_results = get_wine.wine_results(sort_by, varietals, wine_style, wine_type)
    
    sliced = slice(0,10)
    wine_results = wine_results[sliced]
    
    # session['wine_results'] = wine_results
         
    if wine_results == []:
        wine_results = ['No Results']
          
          
    if g.user:
        user_favorites = []
        user_favs = g.user.fav_wines
        for fav in user_favs:
            user_favorites.append(fav.id) 
    else:
        user_favorites = []
        
    
    if g.user:
        reviews = []
        for post in g.user.posts:
            reviews.append(post.wine_id)
    else:
        reviews = []
    
    
    return jsonify(wine_results=wine_results, user_favorites=user_favorites, reviews=reviews)

# ===================================    RECEIVING SORT BY PICKS   =====================================


@app.route('/sort_by/<new_sort_by>')
def get_sort_by_choices(new_sort_by):

    sort_by = session['sort_by']
    
    if new_sort_by in sort_by:
        sort_by.remove(new_sort_by)
    else:    
        sort_by.append(new_sort_by)
        if 'None' in sort_by:
            sort_by.remove('None')
            
    if not len(sort_by):
        sort_by = ['None']
        
    session['sort_by'] = sort_by
    
   

    
    
    # print("###########  wine results ###############")
    # print(session['wine_results'])

    # if session['wine_results'] != ['None']:
    # wine = session['wine_results']
    # sorted_wine = get_wine.sort_results(sort_by, wine)
    # import pdb
    # pdb.set_trace()
    
    # return jsonify(wine_results=sorted_wine)
        
    # else:
    return render_template("new_home.html")
    
    # import pdb
    # pdb.set_trace()

    # return render_template("new_home.html")


# ===================================    SORTING WINE RESULTS   =====================================


# ===================================    SENDING VARIETAL OPTIONS   =====================================

@app.route('/get_varietals')
def get_varietals():

    selected_varietals = session['varietals']
    wine_type = session['wine_type']

    varietals = varietal_cls.get_all_varietals(wine_type)

    return jsonify(varietals=varietals, selected_varietals=selected_varietals)

# ===================================    RECEIVING VARIETAL PICKS   =====================================
    
    
@app.route('/log_varietals/<new_varietal>')
def log_varietal_choice(new_varietal):

    
    varietals = session['varietals']


    # import pdb
    # pdb.set_trace()
    
    if new_varietal in varietals:
        varietals.remove(new_varietal)
    else:
        varietals.append(new_varietal)
        if 'All' in varietals:
            varietals.remove('All')

    
    if session['varietals'] == []:
        session['varietals'] = ['All']
    else:
        session['varietals'] = [wine for wine in varietals]
    
    return jsonify(varietals=varietals)



# ===================================    SHOWING RESULTS   =====================================

@app.route('/show_results')
def show_results():
    
    varietals = session['varietals']
    sort_by = session['sort_by']
    wine_style = session['wine_style']
    wine_type = session['wine_type']

   
    wine_results = get_wine.wine_results(sort_by, varietals, wine_style, wine_type)
    
    session['wine_results'] = wine_results

    # sliced = slice(0,10)
    # sliced_results = wine_results[sliced]
    
    # import pdb
    # pdb.set_trace()
    
    if g.user:
        user_reviews = []
        for post in g.user.posts:
            user_reviews.append(post.wine_id)
    else:
        user_reviews = []
    
    if g.user:
        user_favorites = []
        for fav in g.user.fav_wines:
            user_favorites.append(fav.id)
    else:
        user_favorites = []
    
    if wine_results == []:
        wine_results = ['No Results']
        
        

    return render_template("wine_results.html", wines=wine_results, user_favorites=user_favorites, user_reviews=user_reviews)

# ===================================    SEARCH BAR   =====================================
# @app.route('/search/<search_term>')
# def set_search_results(search_term):
    
 
#     wine_results = get_wine.search_results(search_term)
  
    
#     # import pdb
#     # pdb.set_trace()
    
#     # if wine_results == []:
#     #     wine_results = ['No Results']
#     #     session['search_results'] = wine_results
#     # else:
#     session['search_results'] = wine_results
        
    

 

#     return jsonify(wine_results=wine_results)


@app.route('/search/<search_term>')
def get_search_results(search_term):
    
    # import pdb
    # pdb.set_trace()
    
    if search_term == '':
        wine_results = ['Please add a search value.']
    else:
        wine_results = get_wine.search_results(search_term)
    
    paginated = [wine_results[i:i+9] for i in range(0, len(wine_results), 9)]
    
    
    favs= []
    reviews = []
        
    if g.user:
        for wine in g.user.fav_wines:
            favs.append(wine.id)
    
    if g.user:
        for post in g.user.posts:
            reviews.append(post.wine_id)
 
    # return render_template("search_results.html", wine_results=paginated_wine, user_favorites=favs, user_reviews=reviews)

    return jsonify(paginated=paginated, favs=favs, reviews=reviews)


# @app.route('/search/results')
# def get_search_results():
    
 
#     search_term = session['search_term']
#     wine_results = get_wine.search_results(search_term)
  
    
#     # import pdb
#     # pdb.set_trace()
    
        
    
#     favs= []
#     reviews = []
        
#     if g.user:
#         for fav in g.user.fav_wines:
#             favs.append(fav.id)
    
#     if g.user:
#         for post in g.user.posts:
#             reviews.append(post.wine_id)
 

#     return jsonify(wine_results=wine_results, reviews=reviews, favs=favs)


@app.route('/search')
def show_search_results():
    
 

    # search_term = request.args.get("wine")
    # session['search_term'] = search_term
    
   
    
    # if search_term == '':
    #     wine_results = ['Please add a search value.']
    # else:
    #     wine_results = get_wine.search_results(search_term)

    # # wine_results = session['search_results']
    
    
    
    # favs= []
    # reviews = []
        
    # if g.user:
    #     for wine in g.user.fav_wines:
    #         favs.append(wine.id)
    
    # if g.user:
    #     for post in g.user.posts:
    #         reviews.append(post.wine_id)
            
   
    # # def getrows_byslice(seq, rowlen):
    # #     for start in range(0, len(seq), rowlen):
    # #         seq[start:start+rowlen]
    #     #    mylist[i:i+4] 
    # paginated = [wine_results[i:i+9] for i in range(0, len(wine_results), 9)]
    # paginated_wine = paginated[0]
    
    # session['search_results'] = paginated
    
    # # import pdb
    # # pdb.set_trace()
    

    return render_template("search_results.html")
