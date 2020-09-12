import os
from unittest import TestCase
from sqlalchemy import exc
# from sqlalchemy.exc import IntegrityError
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///wine_test_db"


# Now we can import app

from app import app, CURR_USER_KEY
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from models import db, connect_db, User, Post, Wine, Favorite
import re

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class FlaskTests(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        app.config['TESTING'] = True
        self.client = app.test_client()
        # CREATING A USER

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    ##### Testing User Model
    def test_user_model(self):
        """Does basic model work?"""
        u = User(
            name="testtestname",
            username="testtestusername",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        # TESTS (USER SHOULD HAVE NO POSTED REVIEWS AND NO FAVORITES)
        self.assertEqual(len(u.posts), 0)
        self.assertEqual(len(u.fav_wines), 0)

    def test_complex_user(self):
        """Does u1 contains posts and favorites"""
        self.u1 = User.signup(name="testname", username="testusername", password="testpassword",)
        self.u1_id = 5555
        self.u1.id = self.u1_id
        db.session.commit()
        # ADDING A WINE
        wine1 = Wine(wine_id="0001", winery="winery1", country="USA", area="Santa Barbara", vintage="2020", varietal="Barbera", type="Red", name="first-wine", rating=94.549999999)
        wine1.id = 1
        db.session.add(wine1)
        db.session.commit()
        # ADDING THE WINE TO USER FAVORITES
        fav1 = Favorite(wine_id=wine1.id, user_id=self.u1_id)
        db.session.add(fav1)
        db.session.commit()
        # ADDING A REVIEW FOR THE WINE
        review1 = Post(rating=98, review="My first and most favorite wine", wine_id=wine1.id, user_id=self.u1_id)
        review1.id = 1
        db.session.add(review1)
        db.session.commit()
        # TESTS (USER SHOULD HAVE ONLY 1 FAV WINE AND REVIEW)
        self.assertEqual(len(self.u1.posts), 1)
        self.assertEqual(len(self.u1.fav_wines), 1)
        
    def test_wine_model(self):
        """Does wine model work?"""
        # ADDING WINES
        wine1 = Wine(wine_id="0001", winery="winery1", country="USA", area="Santa Barbara", vintage="2020", varietal="Barbera", type="Red", name="first-wine", rating=89)
        wine1.id = 1
        wine2 = Wine(wine_id="0002", winery="winery2", country="Italy", area="Piedmont", vintage="2019", varietal="Barolo", type="Red", name="second-wine", rating=95)
        wine2.id = 2
        wine3 = Wine(wine_id="0003", winery="winery3", country="France", area="Rhone Valley", vintage="2018", varietal="Syrah", type="Red", name="third-wine", rating=96)
        wine3.id = 3
        wine4 = Wine(wine_id="0004", winery="winery4", country="USA", area="Sonoma", vintage="2017", varietal="Chardonnay", type="White", name="fourth-wine", rating=97)
        wine4.id = 4
        db.session.add_all([wine1, wine2, wine3, wine4])
        db.session.commit()
        # QUERIES
        all_wine = Wine.query.all()
        local_wine = Wine.query.filter(Wine.country=='USA').all()
        all_reds = Wine.query.filter(Wine.type=='Red').all()
        vintage_based = Wine.query.filter(Wine.vintage>'2017').all()
        b_wines = Wine.query.filter(Wine.varietal.ilike('%b%')).all()
        low_ratings = Wine.query.filter(Wine.rating<95).all()
        # TESTS
        self.assertEqual(len(all_wine), 4)
        self.assertEqual(len(local_wine), 2)
        self.assertEqual(len(all_reds), 3)
        self.assertEqual(len(vintage_based), 3)
        self.assertEqual(len(b_wines), 2)
        self.assertEqual(len(low_ratings), 1)

    def test_favorite_model(self):
        """Does favorite model work"""
        #ADDING USERS
        self.u1 = User.signup(name="testname", username="testusername", password="testpassword",)
        self.u1_id = 1111
        self.u1.id = self.u1_id
        self.u2 = User.signup(name="testname2", username="testusername2", password="testpassword2",)
        self.u2_id = 2222
        self.u2.id = self.u2_id
        db.session.commit()
        # ADDING WINES
        wine1 = Wine(wine_id="0001", winery="winery1", country="USA", area="Santa Barbara", vintage="2020", varietal="Barbera", type="Red", name="first-wine", rating=89)
        wine1.id = 1
        wine2 = Wine(wine_id="0002", winery="winery2", country="Italy", area="Piedmont", vintage="2019", varietal="Barolo", type="Red", name="second-wine", rating=95)
        wine2.id = 2
        db.session.add_all([wine1, wine2])
        db.session.commit()
        # ADDING THE WINE TO USERS FAVORITES
        fav1 = Favorite(wine_id=1, user_id=self.u1_id)
        fav2 = Favorite(wine_id=2, user_id=self.u2_id)
        db.session.add_all([fav1, fav2])
        db.session.commit()
        # QUERIES
        favs = Favorite.query.all()
        # TESTS
        self.assertEqual(len(self.u1.fav_wines), 1)
        self.assertEqual(len(self.u2.fav_wines), 1)
        self.assertEqual(len(favs), 2)

    def test_user_model(self):
        """Does user model work"""
        #ADDING USERS
        self.u1 = User.signup(name="testname", username="testusername", password="testpassword",)
        self.u1_id = 1111
        self.u1.id = self.u1_id
        self.u2 = User.signup(name="testname2", username="testusername2", password="testpassword2",)
        self.u2_id = 2222
        self.u2.id = self.u2_id
        db.session.commit()
        # ADDING WINES
        wine1 = Wine(wine_id="0001", winery="winery1", country="USA", area="Santa Barbara", vintage="2020", varietal="Barbera", type="Red", name="first-wine", rating=89)
        wine1.id = 1
        wine2 = Wine(wine_id="0002", winery="winery2", country="Italy", area="Piedmont", vintage="2019", varietal="Barolo", type="Red", name="second-wine", rating=95)
        wine2.id = 2
        wine3 = Wine(wine_id="0003", winery="winery3", country="France", area="Rhone Valley", vintage="2018", varietal="Syrah", type="Red", name="third-wine", rating=96)
        wine3.id = 3
        wine4 = Wine(wine_id="0004", winery="winery4", country="USA", area="Sonoma", vintage="2017", varietal="Chardonnay", type="White", name="fourth-wine", rating=97)
        wine4.id = 4
        db.session.add_all([wine1, wine2, wine3, wine4])
        db.session.commit()
        # ADDING REVIEWS
        review1 = Post(rating=90, review="My first review", wine_id=wine1.id, user_id=self.u1_id)
        review1.id = 1
        review2 = Post(rating=90, review="My second review", wine_id=wine2.id, user_id=self.u2_id)
        review2.id = 2
        review3 = Post(rating=94, review="My third review", wine_id=wine3.id, user_id=self.u2_id)
        review3.id = 3
        review4 = Post(rating=96, review="My fourth review", wine_id=wine4.id, user_id=self.u2_id)
        review4.id = 4
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        # QUERIES
        first_review = Post.query.filter(Post.review=="My first review").all()
        sim_ratings = Post.query.filter(Post.rating==90).all()
        last = Post.query.filter(Post.wine_id==wine4.id).all()
        # TESTS
        self.assertEqual(len(first_review), 1)
        self.assertEqual(len(sim_ratings), 2)
        self.assertEqual(len(last), 1)
        self.assertEqual(len(self.u1.posts), 1)
        self.assertEqual(len(self.u2.posts), 3)
        
  
        
        
        

        

