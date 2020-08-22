
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re



# ===========================================================   'ALL OF THE ABOVE FILTERS'   =========================================================== 
    
    
class AllAbove():
    
    
    def single_varietal(self, sort_by, varietals):
        """Sign up user.

        Hashes password and adds user to system.
        """
        wine_results = []
        
        if sort_by == 'Rating (Highest)':
            wines = Wine.query.order_by(desc(Wine.rating)).all()
            for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
        elif sort_by == 'Rating (Lowest)':
            wines = Wine.query.order_by(Wine.rating).all()
            for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
        elif sort_by == 'Vintage (Oldest)':
            wines = Wine.query.order_by(Wine.vintage).all()
            for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
        elif sort_by == 'Vintage (Youngest)':
            wines = Wine.query.order_by(desc(Wine.vintage)).all()
            for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
        elif sort_by == 'Winery (Alphabetically)':
            wines = Wine.query.order_by(Wine.winery).all()
            for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)

    

# ===========================================================   POST   =========================================================== 


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
    

    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


    

   # ===========================================================   notes   =========================================================== 
 
    
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
