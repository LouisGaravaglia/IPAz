
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from models import db, connect_db, User, Post, Wine, Favorite


class Varietals():
    
    def get_all_varietals(self, varietals):
        """Take a list of varietals and filters through each item to make sure 
        that no elements other than text exist, as well as are certain than
        a certain length and are not empty. Then adds to a set to remove any
        duplicates. Then that list of varietals is returned.
        """     
        varietal_list = []
        varietal_set = set()
        
        # for varietals in merged_varietals:
    #     varietal_list = varietal_list + varietals
    
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
        
        return my_varietals