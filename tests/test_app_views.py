import os
from unittest import TestCase
from sqlalchemy import exc
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///wine_test_db"


# Now we can import app

from app import app, CURR_USER_KEY
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from models import db, connect_db, User, Post, Wine, Favorite

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
        

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_home_page(self):
        """ Making sure that the home page renders correct html. """
        with self.client as client:
            res = self.client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<section class="hero is-info is-bold is-fullheight-with-navbar">', html)
            self.assertIn('<h3 class="title wine-type-title">Choose your wine type</h3>', html)
            self.assertIn('<h3 class="title varietals-title">Choose your varietals</h3>', html)
            self.assertIn('<h3 class="title sort-by-title">Sort your results</h3>', html)
            self.assertIn('<h3 class="title results-btn-title">Find your wines</h3>', html)

    def test_results_page(self):
        """ Making sure that the show wine results page renders correct html. """
        with self.client as client:
            res = self.client.get("/show_results")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">WINE RESULTS</h1>', html)
            self.assertIn('<p id="choose-wine-type" class="sort-label noselect">Wine Types</p>', html)
            self.assertIn('<p id="choose-wine-style" class="sort-label noselect">Wine Style</p>', html)
            self.assertIn('<p id="choose-sort-by" class="sort-label noselect">Sort By</p>', html)
            self.assertIn('<p id="choose-varietals"  class="sort-label noselect">Varietals</p>', html)
            self.assertIn('<div class="columns my-3 mx-3 is-multiline" id="wine-results">', html)
            self.assertIn('<nav class="pagination" role="navigation" aria-label="pagination" id="main-pagination">', html)
            self.assertIn('<p class="modal-card-title">Varietals</p>', html)

    def test_favorites_page(self):
        """ Making sure that the favorites page renders correct html. """
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            res = self.client.get("/user/favorites")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">FAVORITES</h1>', html)
            self.assertIn('<p><strong>NAME: </strong>first-wine</p>', html)
            self.assertIn('<p><strong>WINERY: </strong>winery1</p>', html)
            self.assertIn('<p><strong>COUNTRY: </strong>USA</p>', html)
            self.assertIn('<p><strong>AREA: </strong>Santa Barbara</p>', html)
            self.assertIn('<p><strong>VINTAGE: </strong>2020</p>', html)
            self.assertIn('<p><strong>VARIETAL: </strong>Barbera</p>', html)
            self.assertIn('<p><strong>TYPE: </strong>Red</p>', html)
            ####SUCCESSFULLY ROUNDED RATING OF 94.54999999 TO 94.55
            self.assertIn('<p><strong>RATING: </strong>94.55</p>', html)
            # favorite = Favorite.query.filter(Favorite.wine_id==1).all()
            # self.assertEqual(len(favorite), 1)
            # self.assertEqual(favorite[0].user_id, self.u1_id)


    def test_reviews_page(self):
        """ Making sure that the reviews page renders correct html. """
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            res = self.client.get("/user/reviews")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">REVIEWS</h1>', html)
            self.assertIn('<p><strong>NAME: </strong>first-wine</p>', html)
            self.assertIn('<p><strong>WINERY: </strong>winery1</p>', html)
            self.assertIn('<p><strong>COUNTRY: </strong>USA</p>', html)
            self.assertIn('<p><strong>AREA: </strong>Santa Barbara</p>', html)
            self.assertIn('<p><strong>VINTAGE: </strong>2020</p>', html)
            self.assertIn('<p><strong>VARIETAL: </strong>Barbera</p>', html)
            self.assertIn('<p><strong>TYPE: </strong>Red</p>', html)
            self.assertIn('<p><strong>RATING: </strong>94.55</p>', html)
            self.assertIn('<p><strong>MY RATING: </strong>98</p>', html)
            self.assertIn('<p><strong>REVIEW: </strong>My first and most favorite wine</p>', html)
            # first_review = Post.query.filter(Post.id==1).all()
            # self.assertEqual(len(first_review), 1)
            # self.assertEqual(first_review[0].user_id, self.u1_id)

    def test_profile_page(self):
        """ Making sure that the profile page renders correct html. """
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            res = self.client.get("/user")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            ####HEADERS SHOWING ON PROFILE PAGE
            self.assertIn('<h1 class="title profile-name">', html)
            self.assertIn('<a href="/user/favorites"><p class="title profile-stat">1</p>', html)
            self.assertIn('<a href="/user/reviews"><p class="title profile-stat">1</p>', html)
            self.assertIn('<h2 class="profile-subtitle">Most Recent Favorite</h2>', html)
            self.assertIn('<h2 class="profile-subtitle">Top Rated Review</h2>', html)
            ####FAVORITE SHOWING ON PROFILE PAGE
            self.assertIn('<p><strong>NAME: </strong>first-wine</p>', html)
            self.assertIn('<p><strong>WINERY: </strong>winery1</p>', html)
            self.assertIn('<p><strong>COUNTRY: </strong>USA</p>', html)
            self.assertIn('<p><strong>AREA: </strong>Santa Barbara</p>', html)
            self.assertIn('<p><strong>VINTAGE: </strong>2020</p>', html)
            self.assertIn('<p><strong>VARIETAL: </strong>Barbera</p>', html)
            self.assertIn('<p><strong>TYPE: </strong>Red</p>', html)
            self.assertIn('<p><strong>RATING: </strong>94.55</p>', html)
            ####REVIEW SHOWING ON PROFILE PAGE
            self.assertIn('<p><strong>MY RATING: </strong>98</p>', html)
            self.assertIn('<p><strong>REVIEW: </strong>My first and most favorite wine</p>', html)

    def test_login_page(self):
        """ Making sure that the login page renders correct html. """
        with self.client as client:
            res = self.client.get("/login")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">LOGIN</h1>', html)
            self.assertIn('<form method="POST" id="user_form">', html)
            self.assertIn('<button class="button is-info" type="submit">Submit</button>', html)

    def test_signup_page(self):
        """ Making sure that the signup page renders correct html. """
        with self.client as client:
            res = self.client.get("/signup")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">SIGN UP</h1>', html)
            self.assertIn('<form method="POST" id="user_form">', html)
            self.assertIn('<button class="button is-link" type="submit">Submit</button>', html)

    def test_search_page(self):
        """ Making sure that the search page renders correct html. """
        with self.client as client:
            res = self.client.get("/search")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="block-text">SEARCH RESULTS</h1>', html)
            self.assertIn('<a class="search-pagination-previous button has-text-white is-info">Previous</a>', html)
            self.assertIn('<a class="search-pagination-next button has-text-white is-info">Next</a>', html)
            ####MAKING SURE WINE SHOWS IN JSON RESULTS WHEN SEARCHING FOR BARBERA
            resp = client.get("/search/Barbera", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first-wine', resp.get_data(as_text=True))
            resp = client.get("/search/Barbera", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first-wine', resp.get_data(as_text=True))
            ####NEEDS TO BE CASE AND LENGTH INSENSITIVE
            resp = client.get("/search/bar", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first-wine', resp.get_data(as_text=True))
            resp = client.get("/search/RED", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first-wine', resp.get_data(as_text=True))
            resp = client.get("/search/2020", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first-wine', resp.get_data(as_text=True))
            ####SHOULD NOT RETURN WINE WHEN SEARCH TERMS DO NOT HAVE ANYTHING IN COMMON WITH WINE
            resp = client.get("/search/Cabernet", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('first-wine', resp.get_data(as_text=True))
            resp = client.get("/search/1999", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('first-wine', resp.get_data(as_text=True))
            
           


