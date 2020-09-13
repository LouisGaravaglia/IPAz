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
from get_varietals import Varietals

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()
varietal_cls = Varietals()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class VarietalsTests(TestCase):

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
    def test_get_all_varietals(self):
        """Does get_all_varietals() return the correct varietals based off of wine input"""
        # ADDING WINES
        wine1 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Barbera", type="Red")
        wine1.id = 1
        wine2 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Barolo", type="Red")
        wine2.id = 2
        wine3 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Cabernet", type="Red")
        wine3.id = 3
        wine4 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="syrah", type="Red")
        wine4.id = 4
        wine5 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Noir", type="Red")
        wine5.id = 5
        wine6 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Chardonnay", type="White")
        wine6.id = 6
        wine7 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Gris", type="White")
        wine7.id = 7
        wine8 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Sauvignon Blanc", type="White")
        wine8.id = 8
        wine9 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Riesling", type="White")
        wine9.id = 9
        wine10 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Syrah", type="Rose")
        wine10.id = 10
        wine11 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Grenache", type="Rose")
        wine11.id = 11
        wine12 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Noir", type="Rose")
        wine12.id = 12
        db.session.add_all([wine1, wine2, wine3, wine4, wine5, wine6, wine7, wine8, wine9, wine10, wine11, wine12])
        db.session.commit()
        # TESTING RESULTS
        varietals = varietal_cls.get_all_varietals()
        self.assertIn("Barbera", varietals['red'])
        self.assertIn("Cabernet", varietals['red'])
        self.assertIn("Chardonnay", varietals['white'])
        self.assertIn("Pinot Gris", varietals['white'])
        self.assertIn("Syrah", varietals['rose'])
        self.assertIn("Grenache", varietals['rose'])
        self.assertEqual(len(varietals['red']), 5)
        self.assertEqual(len(varietals['white']), 4)
        self.assertEqual(len(varietals['rose']), 3)
        self.assertNotIn("Barbera", varietals['rose'])
        self.assertNotIn("Cabernet", varietals['white'])
        self.assertNotIn("Chardonnay", varietals['red'])
        self.assertNotIn("Pinot Gris", varietals['red'])
        self.assertNotIn("Syrah", varietals['white'])
        self.assertNotIn("Grenache", varietals['white'])
    
    
   