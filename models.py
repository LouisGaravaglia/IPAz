
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):    
    db.app = app
    db.init_app(app)


# class User(db.Model):
    
#     __tablename__ = "users"
    

#     def __repr__(self):
#         u=self
#         return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"
    
#     id = db.Column(db.Integer,
#                    primary_key = True,
#                    autoincrement = True)
#     first_name = db.Column(db.String(50),
#                      nullable=False)
#     last_name = db.Column(db.String(100))
#     img_url = db.Column(db.String(100),
#                        nullable=False)
#     posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    
#     @property
#     def full_name(self):
#         """Return full name of user."""
        
#         return f"{self.first_name}{self.last_name}"        
    

# class Post(db.Model):
    
#     __tablename__ = "posts"
        
    
#     def __repr__(self):
#         p=self
#         return f"<User id={p.id} title={p.title} content={p.content} created_at={p.created_at} owner_id={p.owner_id}>"
    
#     id = db.Column(db.Integer,
#                    primary_key = True,
#                    autoincrement = True)
#     title = db.Column(db.String(50),
#                      nullable=False)
#     content = db.Column(db.String(1000),
#                      nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
#     owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    
#     @property
#     def friendly_date(self):
#         """Return nicely-formatted date."""
        
#         return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
        
    
# class PostTag(db.Model):
#     """Tag on a post."""

#     __tablename__ = "posts_tags"

#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


# class Tag(db.Model):
#     """Tag that can be added to posts."""

#     __tablename__ = 'tags'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False, unique=True)

#     posts = db.relationship(
#         'Post',
#         secondary="posts_tags",
#         backref="tags",
#     )

# ===========================================================   USER   =========================================================== 
    
    
#     User
# -
# id PK int
# username string
# password string
# bio string

class User(db.Model):
    
    __tablename__ = "users"
    

    def __repr__(self):
        u=self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(2000), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    
    @classmethod
    def signup(cls, name, username, password, bio, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            username=username,
            password=hashed_pwd,
            bio=bio,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


# ===========================================================   POST   =========================================================== 

# Review
# -
# id PK int
# wine_id int FK >- Wine.id
# rating float
# review string
# user_id int FK >- User.id

class Post(db.Model):
    
    __tablename__ = "posts"
        
    
    def __repr__(self):
        p=self
        return f"<User id={p.id} title={p.title} content={p.content} created_at={p.created_at} owner_id={p.owner_id}>"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    rating = db.Column(db.Integer,
                     nullable=False)
    review = db.Column(db.String(5000),
                     nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)    

# ===========================================================   WINE   =========================================================== 
    
# Wine
# -
# id PK int
# winery int
# country string
# vintage string
# varietal string
# wine_style string
# name string
# area string
# description string
# rating float

class Wine(db.Model):
    
    __tablename__ = "wines"
    

    def __repr__(self):
        u=self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    winery = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(100))
    area = db.Column(db.String(100), nullable=False)
    vintage = db.Column(db.String(100))
    varietal = db.Column(db.String(100))
    style = db.Column(db.String(2000), nullable=False)
    type = db.Column(db.String(2000), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    fav_users = db.relationship('User', secondary="favorites", backref="fav_wines")
    
    
    @property
    def full_name(self):
        """Return full name of user."""
        
        return f"{self.first_name}{self.last_name}"  

# ===========================================================   FAVORITES   =========================================================== 

# Saved
# -
# id PK int
# wine_id int FK >- Wine.id
# user_id int FK >- User.id

class Favorite(db.Model):
    
    __tablename__ = "favorites"
    

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


    
# ===========================================================   TAGS   ===========================================================    

# Eye
# -
# id PK int 
# name string

class EyeTag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'eye_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_eye_tags", backref="eye_tags")
    wines = db.relationship('Wine', secondary="wines_eye_tags", backref="eye_tags")

# Nose
# -
# id PK int 
# name string

class NoseTag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'nose_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_nose_tags", backref="nose_tags")
    wines = db.relationship('Wine', secondary="wines_nose_tags", backref="nose_tags")

# Mouth
# -
# id PK int
# name string

class MouthTag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'mouth_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_mouth_tags", backref="mouth_tags")
    wines = db.relationship('Wine', secondary="wines_mouth_tags", backref="mouth_tags")

# Finish
# -
# id PK int 
# name string

class FinishTag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'finish_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary="posts_finish_tags", backref="finish_tags")
    wines = db.relationship('Wine', secondary="wines_finish_tags", backref="finish_tags")

# ===========================================================   POST TAGS   =========================================================== 

# PostEyeTag
# -
# post_id int FK >- Review.id
# tag_id int FK >- Eye.id

class PostEyeTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_eye_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('eye_tags.id'), primary_key=True)
   

# PostNoseTag
# -
# post_id int FK >- Review.id
# tag_id int FK >- Nose.id

class PostNoseTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_nose_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('nose_tags.id'), primary_key=True)

# PostMouthTag
# -
# post_id int FK >- Review.id
# tag_id int FK >- Mouth.id

class PostMouthTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_mouth_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('mouth_tags.id'), primary_key=True)

# PostFinishTag
# -
# post_id int FK >- Review.id
# tag_id int FK >- Finish.id

class PostFinishTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_finish_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('finish_tags.id'), primary_key=True)

# ===========================================================   WINE TAGS   =========================================================== 


# WineEyeTag
# -
# wine_id int 
# tag_id int 

class WineEyeTag(db.Model):
    """Tag on a post."""

    __tablename__ = "wines_eye_tags"

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('eye_tags.id'), primary_key=True)

# WineNoseTag
# -
# wine_id int 
# tag_id int 

class WineNoseTag(db.Model):
    """Tag on a post."""

    __tablename__ = "wines_nose_tags"

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('nose_tags.id'), primary_key=True)

# WineMouthTag
# -
# wine_id int 
# tag_id int 

class WineMouthTag(db.Model):
    """Tag on a post."""

    __tablename__ = "wines_mouth_tags"

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('mouth_tags.id'), primary_key=True)

# WineFinishTag
# -
# wine_id int
# tag_id int

class WineFinishTag(db.Model):
    """Tag on a post."""

    __tablename__ = "wines_finish_tags"

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('finish_tags.id'), primary_key=True)


   # ===========================================================   notes   =========================================================== 
 
      
    # def greet(self):
    #     return f"Hi, my name is {self.name} and i'm a {self.species}!"
    
    # def feed(self, amt=20):
    #     """Update hunger based off of amt"""
        
    #     self.hunger -= amt
    #     self.hunger = max(self.hunger, 0)
    
    # to run this class use the following
    # ipython3
    # %run app.py
    # db.create_all()
    
    # if you add or update the table and then want to update it,
    # you need to go to the Postgres Shell and run DROP table_name,
    # then re run db.create_all()
    
    # Then make sure you import the class name in your app.py file
    
    # To create a instance of this class, type this in ipython, do the follwoing:
    # stevie = Pet(name="Stevie Chicks", species="Chicken", hunger=13)
    
    # then you can use, stevie.name, stevie.hunger, stevie.SMTPRecipientsRefused
    
    # then to sync all of the pets youve created once your done, do the following:
    # db.session.add(stevie)
    # db.session.commit()
    
    # to create a lot of instances at once, you can do the following using sip:
    # names = ['Sushi', 'scout', 'piggie', 'carrot face']
    # species = ['pig', 'cat', 'bunny', 'bunny']
    # pets = [Pet(name=n, species=s) for n,s in zip(names, species)]
    # db.session.add_all(pets) *add_all needs to be ZipFile The class for reading and writing ZIP files.  See section 
    # db.session.commit()
