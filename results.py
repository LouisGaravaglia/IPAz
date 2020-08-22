
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from models import db, connect_db, User, Post, Wine, Favorite



# ===========================================================   'ALL OF THE ABOVE FILTERS'   =========================================================== 
    
    
class AllAbove():
    
    # def __init__(self, wine_style):
    #         self.wine_style = wine_style
    
    def single_varietal(self, sort_by, varietals):
        """Sign up user.

        Hashes password and adds user to system.
        """
          
    
        wine_results = []
        
        if sort_by == 'Rating (Highest)':
            wines = Wine.query.order_by(desc(Wine.rating)).all()
            
        elif sort_by == 'Rating (Lowest)':
            wines = Wine.query.order_by(Wine.rating).all()
            
        elif sort_by == 'Vintage (Oldest)':
            wines = Wine.query.order_by(Wine.vintage).all()
            
        elif sort_by == 'Vintage (Youngest)':
            wines = Wine.query.order_by(desc(Wine.vintage)).all()
            
        elif sort_by == 'Winery (Alphabetically)':
            wines = Wine.query.order_by(Wine.winery).all()
            
        for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
                        
        return wine_results
    
    
    
    def blends(self, sort_by, varietals):
        """Sign up user.

        Hashes password and adds user to system.
        """
          
    
        wine_results = []
        
        if sort_by == 'Rating (Highest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(desc(Wine.rating)).all()
        
        elif sort_by == 'Rating (Lowest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.rating).all()
         
        elif sort_by == 'Vintage (Oldest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.vintage).all()
       
        elif sort_by == 'Vintage (Youngest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(desc(Wine.vintage)).all()
                
        elif sort_by == 'Winery (Alphabetically)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.winery).all()
     
        for result in results:
                    wine_results.append(result)
                    
        return wine_results

# ===========================================================   POST   =========================================================== 


