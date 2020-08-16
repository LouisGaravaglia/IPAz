from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from random import choice, randint
from unittest import TestCase
import requests
from flask_cors import CORS
from secrets import API_KEY
from flask_debugtoolbar import DebugToolbarExtension
from forms import ReviewForm, UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Post, Wine, Favorite
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


# ===================================    HOME    =====================================


@app.route('/')
def homepage():
    """Show homepage"""
    
    return render_template("home.html")


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


# ===================================    USER PAGE / USERS    =====================================


@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, messages=messages)


@app.route('/users/likes')
def show_likes():
    """Show user profile."""

    likes = g.user.likes

  
    return render_template('users/likes.html', likes=likes)


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@app.route("/users/add_like/<int:message_id>", methods=['POST'])
def add_like(message_id):
    """Add the liked message user id to a list."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    liked_message = Message.query.get_or_404(message_id)
    if liked_message.user_id == g.user.id:
        flash("You can't like your own warbles.", "danger")
        return redirect("/")
    
    user_likes = g.user.likes
    
    if liked_message in user_likes:
        g.user.likes = [like for like in user_likes if like != liked_message]
    else:
        g.user.likes.append(liked_message)
        
    db.session.commit()

    return redirect("/")


# ===================================    EDIT/DELETE USER    =====================================


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/warbler-hero.jpg"
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


# ===================================    ADD POSTS    =====================================


@app.route('/<int:user_id>/add_post')
def add_post_page(user_id):
    """shows the form to add a post"""  
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("add_post.html", user=user, tags=tags)

@app.route('/<int:user_id>/add_post', methods=["POST"])
def create_post(user_id):
    """use a form to create a user"""  
    
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the post when user clicks on the post title"""  
      
    post = Post.query.get_or_404(post_id)

    return render_template("show_post.html", post=post)


# ===================================    EDIT/DELETE POSTS    =====================================


@app.route('/posts/<int:post_id>/edit_post')
def show_edit_post_page(post_id):
    """shows the form to edit an existing post"""  
    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit_post', methods=["POST"])
def edit_user_post(post_id):
    """use a form to update and edit a post""" 

    post = Post.query.get_or_404(post_id)

    if request.form["title"] != "" and request.form["title"] !=  None:
        post.title = request.form["title"]
    
    if request.form["content"] != "" and request.form["content"] != None:
        post.content = request.form["content"]
   
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete_post')
def delete_user_post(post_id):
    """delete a post from the database"""  

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")

# ===================================    CREATE TAGS    =====================================

@app.route('/create_tag')
def show_create_tag_page():
    """shows the form to create a tag to then add to posts."""  
    
    tags = Tag.query.all()

    return render_template("create_tag.html", tags=tags)

@app.route('/create_tag', methods=["POST"])
def create_tag_post():
    """use a form to create a tag and update the tag db."""  
    
    tag_name = request.form['tag_name']
    
    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()
   
    return redirect("/create_tag")

# ===================================    SHOW POSTS BY TAG    =====================================

@app.route('/tags/<int:tag_id>')
def show_posts_by_tag_id(tag_id):
    """shows all posts related to a particular tag"""  
    
    tag = Tag.query.get_or_404(tag_id)
 
    return render_template("tag_specific_posts.html", tag=tag)


# ===================================    API CALLS    =====================================

@app.route('/api/get_red_wines')
def get_red_wines():
    """Get all top rated red wines from the API"""  
    
    baseURL = "https://quiniwine.com/api/pub/wineCategory/tre/0/10"
    headers = {'authorization': API_KEY}
    
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    
    # import pdb
    # pdb.set_trace()
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

    baseURL = "https://quiniwine.com/api/pub/wineCategory/twh/0/10"
    headers = {'authorization': API_KEY}
    
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    
    # import pdb
    # pdb.set_trace()
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

    baseURL = "https://quiniwine.com/api/pub/wineCategory/tro/0/10"
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

# ===================================    WINE TYPE OPTIONS   =====================================


@app.route('/show_red_options')
def show_red_options():
    
    mylist = []
    varietals = set()
    
    all_options = [red.varietal.split(",") for red in Wine.query.filter_by(type='Red').all()]
    
    for options in all_options:
        mylist = mylist + options
    
    for item in mylist:
        varietals.add(item.strip())
        
    return render_template("red_options.html", varietals=varietals)

    

# ===================================    WINE RESULTS   =====================================


@app.route('/show_all_white')
def show_all_white_wine():
    all_white = Wine.query.filter_by(type='White').all()
    
    return render_template("white_wine.html", all_white=all_white)