
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from get_varietals import Varietals
from models import db, connect_db, User, Post, Wine, Favorite



# ===========================================================   'ALL OF THE ABOVE RESULTS'   =========================================================== 

    
class WineResults():
    
    def wine_results(self, sort_by, varietals, wine_style, wine_type_list):
        """Returns wine results if the parameters include:

        'All of the above' for wine type and 'Single Varietals' for wine style.
        
        Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
        to then be returned based of the varietals chosen.
        """     
        varietal_cls = Varietals()
        
        wine_results = []
        
        if varietals == ['All']:
            varietals = varietal_cls.get_all_varietals(wine_type_list)
                    
        
        # import pdb
        # pdb.set_trace()
        
        for wine_type in wine_type_list:
        
            ################# GETTING RESULTS FOR RED WINE TYPE #################
            
            if wine_type == 'Red':
                
                for varietal in varietals:
                    results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'Red'))).all()
                    
                    for style in wine_style:
                        if style == 'Single Varietals':
                            for result in results:
                                if re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                    
                        elif style == 'Blends':
                            for result in results:
                                if not re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                
                        else:
                            for result in results:
                                wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                wine_results.append(wine)
            
            ################# GETTING RESULTS FOR WHITE WINE TYPE #################
                        
            elif wine_type == 'White':
                
                for varietal in varietals:
                    results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'White'))).all()
                    
                    for style in wine_style:
                        if style == 'Single Varietals':
                            for result in results:
                                if re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                    
                        elif style == 'Blends':
                            for result in results:
                                if not re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                
                        else:
                            for result in results:
                                wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                wine_results.append(wine)
                
            ################# GETTING RESULTS FOR ROSE WINE TYPE #################
                        
            elif wine_type == 'Rose':
                
                for varietal in varietals:
                    results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'Rose'))).all()
                    
                    for style in wine_style:
                        if style == 'Single Varietals':
                            for result in results:
                                if re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                    
                        elif style == 'Blends':
                            for result in results:
                                if not re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                
                        else:
                            for result in results:
                                wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                wine_results.append(wine)
                    
            ################# GETTING RESULTS FOR ALL WINE TYPES #################

            elif wine_type == 'All of the above':
                
                for varietal in varietals:
                    results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).all()
                    
                    for style in wine_style:
                        if style == 'Single Varietals':
                            for result in results:
                                if re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                    
                        elif style == 'Blends':
                            for result in results:
                                if not re.search(r"^" + varietal + r"$", result.varietal):
                                    wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                    wine_results.append(wine)
                                
                        else:
                            for result in results:
                                wine = {'ID':result.id, 'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                                wine_results.append(wine)
                
        ################# REMOVING DUPLICATES #################
        
        # import pdb
        # pdb.set_trace()
         
        wine_results = [dict(s) for s in set(frozenset(d.items()) for d in wine_results)]
        
        ################# SORTING #################
        
        if 'None' in sort_by:
            return wine_results
        
        for key in sort_by:
                         
            if key == 'Rating (Highest)':                   
                def filter(e):
                    return e['Rating']
                wine_results.sort(key=filter, reverse=True)
            
            if key == 'Rating (Lowest)':
                def filter(e):
                    return e['Rating']
                wine_results.sort(key=filter)
                    
            if key == 'Vintage (Oldest)':
                def filter(e):
                    return e['Vintage']
                wine_results.sort(key=filter)
                    
            if key == 'Vintage (Youngest)':
                def filter(e):
                    return e['Vintage']
                wine_results.sort(key=filter, reverse=True)
                              
            if key == 'Winery (Alphabetically)':
                def filter(e):
                    return e['Winery']
                wine_results.sort(key=filter)
                
        # import pdb
        # pdb.set_trace() 
                      
        return wine_results
    
    
   