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
from results import WineResults

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()
get_wine = WineResults()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class WineResultsTests(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        app.config['TESTING'] = True
        self.client = app.test_client()
        # ADDING WINES
        wine1 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Barbera, Grenache", type="Red", rating=77)
        wine1.id = 1
        wine2 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Barolo", type="Red", rating=74)
        wine2.id = 2
        wine3 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Cabernet, Syrah", type="Red", rating=71)
        wine3.id = 3
        wine4 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="syrah", type="Red", rating=71)
        wine4.id = 4
        wine5 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Noir", type="Red", rating=93)
        wine5.id = 5
        wine6 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Chardonnay, Chenin Blanc", type="White", rating=87)
        wine6.id = 6
        wine7 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Gris", type="White", rating=91)
        wine7.id = 7
        wine8 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Sauvignon Blanc", type="White", rating=89)
        wine8.id = 8
        wine9 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Riesling", type="White", rating=78)
        wine9.id = 9
        wine10 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Syrah", type="Rose", rating=54)
        wine10.id = 10
        wine11 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Grenache, Syrah, Pinot Noir", type="Rose", rating=85)
        wine11.id = 11
        wine12 = Wine(wine_id="1001", winery="my_winery", name="my_name", varietal="Pinot Noir", type="Rose", rating=99)
        wine12.id = 12
        db.session.add_all([wine1, wine2, wine3, wine4, wine5, wine6, wine7, wine8, wine9, wine10, wine11, wine12])
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    ##### Testing User Model
    def test_all_of_above(self):
        """Does having no filters chosen return all wines"""
        all_varietals = ['All']
        all_type = ['All of the above']
        all_style = ['All']
        all_results = get_wine.wine_results(all_varietals, all_style, all_type)
        self.assertEqual(len(all_results), 12)
        
    def test_wine_type(self):
        """Does the specific wine type return only those wines with that wine type"""
        # SETTING UP VARIABLES
        type_specific_varietals = ["Syrah", "Pinot Noir"]
        type_specific_type = ['Red']
        type_specific_style = ['All']
        type_red_varietals = ['All']
        type_red_type = ['Red']
        type_red_style = ['All']
        type_white_varietals = ['All']
        type_white_type = ['White']
        type_white_style = ['All']
        type_rose_varietals = ['All']
        type_rose_type = ['Rose']
        type_rose_style = ['All']
        # RESULTS
        wine_results_specific_type = get_wine.wine_results(type_specific_varietals, type_specific_style, type_specific_type)
        wine_results_red_type = get_wine.wine_results(type_red_varietals, type_red_style, type_red_type)
        wine_results_white_type = get_wine.wine_results(type_white_varietals, type_white_style, type_white_type)
        wine_results_rose_type = get_wine.wine_results(type_rose_varietals, type_rose_style, type_rose_type)
        # TESTS
        self.assertEqual(len(wine_results_specific_type), 3)
        self.assertEqual(len(wine_results_red_type), 5)
        self.assertEqual(len(wine_results_white_type), 4)
        self.assertEqual(len(wine_results_rose_type), 3)
        
    def test_wine_style(self):
        """Does having a specific wine style selected return only wines with that wine style"""
        # SETTING UP VARIABLES
        single_varietals = ["Pinot Noir"]
        single_type = ['Rose']
        single_style = ['Single Varietals']
        blend_varietals = ["Pinot Noir"]
        blend_type = ['Rose']
        blend_style = ['Blends']
        all_style_varietals = ["Pinot Noir"]
        all_style_type = ['Rose']
        all_style = ['ALL']
        # RESULTS
        single_style_results = get_wine.wine_results(single_varietals, single_style, single_type)
        blend_style_results = get_wine.wine_results(blend_varietals, blend_style, blend_type)
        all_style_results = get_wine.wine_results(all_style_varietals, all_style, all_style_type)
        # TESTS
        self.assertEqual(len(single_style_results), 1)
        self.assertEqual(len(blend_style_results), 1)
        self.assertEqual(len(all_style_results), 2)
        
    def test_vareitals(self):
        """Making sure that mulitple versions of the same varietal will return same results"""
        # SETTING UP VARIABLES
        capital_varietal = ["Syrah"]
        capital_type = ['All of the above']
        capital_style = ['All']
        lowercase_varietal = ["syrah"]
        lowercase_type = ['All of the above']
        lowercase_style = ['All']
        shortened_varietal = ["sy"]
        shortened_type = ['All of the above']
        shortened_style = ['All']
        # RESULTS
        capital_results = get_wine.wine_results(capital_varietal, capital_style, capital_type)
        lowercase_results = get_wine.wine_results(lowercase_varietal, lowercase_style, lowercase_type)
        shortened_results = get_wine.wine_results(shortened_varietal, shortened_style, shortened_type)
        # TESTS
        self.assertEqual(len(capital_results), 4)
        self.assertEqual(len(lowercase_results), 4)
        self.assertEqual(len(shortened_results), 4)


    
    
   