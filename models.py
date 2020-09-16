
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# ===========================================================   USER   =========================================================== 

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @classmethod
    def signup(cls, name, username, password):
        """Sign up user.
        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            name=name,
            username=username,
            password=hashed_pwd
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

class Post(db.Model):
    __tablename__ = "posts"
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

class Wine(db.Model):
    __tablename__ = "wines"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    wine_id = db.Column(db.String(200), nullable=False)
    winery = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200))
    area = db.Column(db.String(200))
    vintage = db.Column(db.String(200))
    varietal = db.Column(db.String(200))
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    fav_users = db.relationship('User', secondary="favorites", backref="fav_wines")
    
    def serialize(self):
        return {
            'id': self.id,
            'wine_id': self.wine_id,
            'winery': self.winery,
            'country': self.country,
            'area': self.area,
            'vintage': self.vintage,
            'varietal': self.varietal,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'rating': self.rating
        }

# ===========================================================   FAVORITES   =========================================================== 

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)