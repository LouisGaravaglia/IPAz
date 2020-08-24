
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from models import db, connect_db, User, Post, Wine, Favorite



# ===========================================================   'ALL OF THE ABOVE RESULTS'   =========================================================== 
    
    
class AllAbove():
    
    def single_varietal(self, filter_dict, varietals):
        """Returns wine results if the parameters include:

        'All of the above' for wine type and 'Single Varietals Only' for wine style.
        
        Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
        to then be returned based of the varietals chosen.
        """     
    
        wine_results = []
        
        if filter_dict['Rating (Highest)']:
            wines = Wine.query.order_by(desc(Wine.rating)).all()
            
        elif filter_dict['Rating (Lowest)']:
            wines = Wine.query.order_by(Wine.rating).all()
            
        elif filter_dict['Vintage (Oldest)']:
            wines = Wine.query.order_by(Wine.vintage).all()
            
        elif filter_dict['Vintage (Youngest)']:
            wines = Wine.query.order_by(desc(Wine.vintage)).all()
            
        elif filter_dict['Winery (Alphabetically)']:
            wines = Wine.query.order_by(Wine.winery).all()
            
        for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
                        
        return wine_results
    
    
    
    def all_wines(self, filter_dict, varietals):
        """Returns wine results if the parameters include:

        'All of the above' for wine type and 'Blends As Well' for wine style.
        
        Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
        to then be returned based of the varietals chosen.
        """
          
        wine_results = []
        
        # import pdb
        # pdb.set_trace()
        
        # if filter_dict['Red']:
        #     red_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        
        # if filter_dict['White']:
        #     white_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        
        # if filter_dict['Rose']:
        #     rose_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
        
        # if not filter_dict['Red'] and not filter_dict['White'] and not filter_dict['Rose'] or filter_dict['All of the above']:
        #     all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]
        
        # merged_varietals = red_varietals + white_varietals + rose_varietals + all_varietals
    
    #    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # wine_id = db.Column(db.String(200), nullable=False)
    # winery = db.Column(db.String(200), nullable=False)
    # country = db.Column(db.String(200))
    # area = db.Column(db.String(200))
    # vintage = db.Column(db.String(200))
    # varietal = db.Column(db.String(200))
    # type = db.Column(db.String(30), nullable=False)
    # name = db.Column(db.String(200), nullable=False)
    # description = db.Column(db.String(500))
    # rating = db.Column(db.Float)
    
    # Lists to represent keys and values 
# keys = ['a','b','c','d','e'] 
# values = [1,2,3,4,5]   
  
# # but this line shows dict comprehension here   
# myDict = { k:v for (k,v) in zip(keys, values)}   

        
        if filter_dict['Rating (Highest)']:
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).all()
                for result in results:
                    wine = {'Rating':result.rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}                  
                    wine_results.append(wine)
                            
            def myFunc(e):
                return e['Rating']
            wine_results.sort(key=myFunc, reverse=True)
            
        
                
                    
        elif filter_dict['Rating (Lowest)']:
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.rating).all()
                for result in results:
                    wine_results.append(result)
                    
        elif filter_dict['Vintage (Oldest)']:
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.vintage).all()
                for result in results:
                    wine_results.append(result)
                    
        elif filter_dict['Vintage (Youngest)']:
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(desc(Wine.vintage)).all()
                for result in results:
                    wine_results.append(result)
                              
        elif filter_dict['Winery (Alphabetically)']:
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.winery).all()
                for result in results:
                    wine_results.append(result)
        
        # import pdb
        # pdb.set_trace() 
                  
        return wine_results

# ===========================================================   RED WHITE ROSE RESULTS  =========================================================== 


class RedWhiteRose():
    
    def single_varietal(self, wine_type, sort_by, varietals):
        """Returns wine results if the parameters include:

        'Red', 'White', or 'Rose' for wine type and 'Single Varietals Only' for wine style.
        
        Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
        to then be returned based of the varietals chosen.
        """      
    
        wine_results = []
        
        if sort_by == 'Rating (Highest)':
            wines = Wine.query.filter_by(type=wine_type).order_by(desc(Wine.rating)).all()
            
        elif sort_by == 'Rating (Lowest)':
            wines = Wine.query.filter_by(type=wine_type).order_by(Wine.rating).all()     
            
        elif sort_by == 'Vintage (Oldest)':
            wines = Wine.query.filter_by(type=wine_type).order_by(Wine.vintage).all()
            
        elif sort_by == 'Vintage (Youngest)':
            wines = Wine.query.filter_by(type=wine_type).order_by(desc(Wine.vintage)).all()
            
        elif sort_by == 'Winery (Alphabetically)':
            wines = Wine.query.filter_by(type=wine_type).order_by(Wine.winery).all()
            
        for wine in wines:
                varietal_description = wine.varietal
                for varietal in varietals:
                    if re.search(r"^" + varietal + r"$", varietal_description):
                        wine_results.append(wine)
                        
        return wine_results
    
    
    
    def blends(self, wine_type, sort_by, varietals):
        """Returns wine results if the parameters include:

        'Red', 'White', or 'Rose' for wine type and 'Blends As Well' for wine style.
        
        Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
        to then be returned based of the varietals chosen.
        """ 
    
        wine_results = []
        
        if sort_by == 'Rating (Highest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(desc(Wine.rating)).all()
        
        elif sort_by == 'Rating (Lowest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.rating).all()
         
        elif sort_by == 'Vintage (Oldest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.vintage).all()
       
        elif sort_by == 'Vintage (Youngest)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(desc(Wine.rating)).order_by(desc(Wine.vintage)).all()
                
        elif sort_by == 'Winery (Alphabetically)':
            for varietal in varietals:
                results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.winery).all()
     
        for result in results:
                    wine_results.append(result)
                    
        return wine_results
    
    
    
    # ===================== ORIGINAL CODE BEFORE I TRIED USING FILTER_DICT =====================
    
    
    
# from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
# from sqlalchemy import desc
# import re
# from models import db, connect_db, User, Post, Wine, Favorite



# # ===========================================================   'ALL OF THE ABOVE RESULTS'   =========================================================== 
    
    
# class AllAbove():
    
#     def single_varietal(self, sort_by, varietals):
#         """Returns wine results if the parameters include:

#         'All of the above' for wine type and 'Single Varietals Only' for wine style.
        
#         Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
#         to then be returned based of the varietals chosen.
#         """     
    
#         wine_results = []
        
#         if sort_by == 'Rating (Highest)':
#             wines = Wine.query.order_by(desc(Wine.rating)).all()
            
#         elif sort_by == 'Rating (Lowest)':
#             wines = Wine.query.order_by(Wine.rating).all()
            
#         elif sort_by == 'Vintage (Oldest)':
#             wines = Wine.query.order_by(Wine.vintage).all()
            
#         elif sort_by == 'Vintage (Youngest)':
#             wines = Wine.query.order_by(desc(Wine.vintage)).all()
            
#         elif sort_by == 'Winery (Alphabetically)':
#             wines = Wine.query.order_by(Wine.winery).all()
            
#         for wine in wines:
#                 varietal_description = wine.varietal
#                 for varietal in varietals:
#                     if re.search(r"^" + varietal + r"$", varietal_description):
#                         wine_results.append(wine)
                        
#         return wine_results
    
    
    
#     def blends(self, sort_by, varietals):
#         """Returns wine results if the parameters include:

#         'All of the above' for wine type and 'Blends As Well' for wine style.
        
#         Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
#         to then be returned based of the varietals chosen.
#         """
          
#         wine_results = []
        
#         if sort_by == 'Rating (Highest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(desc(Wine.rating)).all()
        
#         elif sort_by == 'Rating (Lowest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.rating).all()
         
#         elif sort_by == 'Vintage (Oldest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.vintage).all()
       
#         elif sort_by == 'Vintage (Youngest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(desc(Wine.vintage)).all()
                
#         elif sort_by == 'Winery (Alphabetically)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%'))).order_by(Wine.winery).all()
     
#         for result in results:
#                     wine_results.append(result)
                    
#         return wine_results

# # ===========================================================   RED WHITE ROSE RESULTS  =========================================================== 


# class RedWhiteRose():
    
#     def single_varietal(self, wine_type, sort_by, varietals):
#         """Returns wine results if the parameters include:

#         'Red', 'White', or 'Rose' for wine type and 'Single Varietals Only' for wine style.
        
#         Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
#         to then be returned based of the varietals chosen.
#         """      
    
#         wine_results = []
        
#         if sort_by == 'Rating (Highest)':
#             wines = Wine.query.filter_by(type=wine_type).order_by(desc(Wine.rating)).all()
            
#         elif sort_by == 'Rating (Lowest)':
#             wines = Wine.query.filter_by(type=wine_type).order_by(Wine.rating).all()     
            
#         elif sort_by == 'Vintage (Oldest)':
#             wines = Wine.query.filter_by(type=wine_type).order_by(Wine.vintage).all()
            
#         elif sort_by == 'Vintage (Youngest)':
#             wines = Wine.query.filter_by(type=wine_type).order_by(desc(Wine.vintage)).all()
            
#         elif sort_by == 'Winery (Alphabetically)':
#             wines = Wine.query.filter_by(type=wine_type).order_by(Wine.winery).all()
            
#         for wine in wines:
#                 varietal_description = wine.varietal
#                 for varietal in varietals:
#                     if re.search(r"^" + varietal + r"$", varietal_description):
#                         wine_results.append(wine)
                        
#         return wine_results
    
    
    
#     def blends(self, wine_type, sort_by, varietals):
#         """Returns wine results if the parameters include:

#         'Red', 'White', or 'Rose' for wine type and 'Blends As Well' for wine style.
        
#         Also, takes in the sort_by filter the user chose and will filter the results from a SQL Alchemy query 
        
#         to then be returned based of the varietals chosen.
#         """ 
    
#         wine_results = []
        
#         if sort_by == 'Rating (Highest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(desc(Wine.rating)).all()
        
#         elif sort_by == 'Rating (Lowest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.rating).all()
         
#         elif sort_by == 'Vintage (Oldest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.vintage).all()
       
#         elif sort_by == 'Vintage (Youngest)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(desc(Wine.rating)).order_by(desc(Wine.vintage)).all()
                
#         elif sort_by == 'Winery (Alphabetically)':
#             for varietal in varietals:
#                 results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == wine_type))).order_by(Wine.winery).all()
     
#         for result in results:
#                     wine_results.append(result)
                    
#         return wine_results