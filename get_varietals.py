
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from models import db, connect_db, User, Post, Wine, Favorite


class Varietals():
    
    def get_all_varietals(self, wine_type):
        """Take a list of varietals and filters through each item to make sure 
        that no elements other than text exist, as well as are certain than
        a certain length and are not empty. Then adds to a set to remove any
        duplicates. Then that list of varietals is returned.
        """     
        varietal_list = []
        varietal_set = set()
        red_varietals = []
        white_varietals = []
        rose_varietals = []
        all_varietals = []
        
        if 'Red' in wine_type:
            red_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        
        if 'White' in wine_type:
            white_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        
        if 'Rose' in wine_type:
            rose_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
            
        if (not 'Red' in wine_type and not 'White' in wine_type and not 'Rose' in wine_type) or 'All of the above' in wine_type:
            all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]
            
        varietals = red_varietals + white_varietals + rose_varietals + all_varietals
            
    
        for varietal in varietals:
            varietal_list = varietal_list + varietal
    
        
        
        for item in varietal_list:
            has_number = re.search("\d", item)
            has_blend = re.search(" Blend", item)
            has_plus = re.search("\+", item)
            has_slash = re.search("/", item)
            has_period = re.search("\.", item)
            has_ampersand = re.search("&", item)
        
            conditions = [has_number, has_blend, has_plus, has_slash, has_period, has_ampersand]
        
            if item != "" and len(item) < 25 and not any(conditions):
                title_case_item = item.title()
                varietal_set.add(title_case_item.strip())
   
        # import pdb
        # pdb.set_trace()
        
        my_varietals = [varietal for varietal in varietal_set]
        
        sorted_list = sorted(my_varietals)
        
        return sorted_list