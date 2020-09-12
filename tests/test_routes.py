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
    
    # def test_login_page(self):
    #     """ Making sure that the login page renders correct html. """
    #     with self.client as client:
    #         res = self.client.get("/login", follow_redirects=True)
    #         html = res.get_data(as_text=True)
    #         self.assertEqual(res.status_code, 200)            
    #         self.assertIn('Invalid credentials.',
    #                 res.get_data(as_text=True))

    
    # def test_signup_page(self):
    #     """ Making sure that the signup page renders correct html. """
    #     with self.client as client:
    #         with client.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.u1_id
                
    #             res = self.client.get("/signup")
    #             html = res.get_data(as_text=True)
    #             self.assertEqual(res.status_code, 200)
                
    #             invalid = User.signup(name="testname", username="testusername", password="testpassword",)
    #             uid = 123789
    #             invalid.id = uid
    #             with self.assertRaises(exc.IntegrityError) as context:
    #                 db.session.commit()
            
            # u2 = User.signup(name="testname", username="testusername", password="testpassword",)
            
            # with self.assertRaises(IntegrityError):
            #     db.session.commit()
            
            
    ##### Signup Tests
            
    def test_valid_signup(self):
        u_test = User.signup("testtestname", "testtestusername", "testtestpassword")
        uid = 99999
        u_test.id = uid
        db.session.commit()
        
        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtestusername")
        self.assertEqual(u_test.name, "testtestname")
        self.assertNotEqual(u_test.password, "testtestpassword")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))
        
    def test_invalid_username_signup(self):
        invalid = User.signup("testtestname", None, "testtestpassword")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_name_signup(self):
        invalid = User.signup(None, "testtestusername", "testtestpassword")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtestname", "testtestusername", "")
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtestname", "testtestusername", None)
            
    ##### Authentication Tests
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "testpassword")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1_id)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "testpassword"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))



    
       


