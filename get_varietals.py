
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from models import db, connect_db, User, Post, Wine, Favorite


class Varietals():
    
    def get_all_varietals(self):
        """Take a list of varietals and filters through each item to make sure 
        that no elements other than text exist, as well as are certain than
        a certain length and are not empty. Then adds to a set to remove any
        duplicates. Then that list of varietals is returned.
        """     
        
       
        
        varietal_dict = {}
        red_varietal_set = set()
        rose_varietal_set = set()
        white_varietal_set = set()
        all_varietal_set = set()
        # red_varietals = []
        # white_varietals = []
        # rose_varietals = []
        # all_varietals = []
        
        # if 'Red' in wine_type:
        reds = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        red_flat_list = [varietal for sublist in reds for varietal in sublist]
        varietal_dict.update({"red":red_flat_list})
        
        # if 'White' in wine_type:
        whites = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        white_flat_list = [varietal for sublist in whites for varietal in sublist]
        varietal_dict.update({"white":white_flat_list})
        # if 'Rose' in wine_type:
        roses = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
        rose_flat_list = [varietal for sublist in roses for varietal in sublist]
        varietal_dict.update({"rose":rose_flat_list})
        # if (not 'Red' in wine_type and not 'White' in wine_type and not 'Rose' in wine_type) or 'All of the above' in wine_type:
        alls = [wine.varietal.split(",") for wine in Wine.query.all()]
        all_flat_list = [varietal for sublist in alls for varietal in sublist]
        varietal_dict.update({"all":all_flat_list}) 
        # varietals = red_varietals + white_varietals + rose_varietals + all_varietals
         
        # import pdb
        # pdb.set_trace()    
    
        # for varietal in red_varietals:
        #     varietal_list = varietal_list + varietal
    
        for key,items in varietal_dict.items():
            
            for item in items:
                has_number = re.search("\d", item)
                has_blend = re.search(" Blend", item)
                has_plus = re.search("\+", item)
                has_slash = re.search("/", item)
                has_period = re.search("\.", item)
                has_ampersand = re.search("&", item)
                has_double_chardonay = re.search(r"^" + "Chardonnay Chardonnay" + r"$", item)
                has_chardonay_pinot = re.search(r"^" + "Chardonnay Pinot Noir" + r"$", item)
                has_chenin_chardonay = re.search(r"^" + "Chenin Blanc Chardonnay" + r"$", item)
                has_cabf_syrah = re.search(r"^" + "Cabernet Franc Syrah" + r"$", item)
                has_cab_malbec = re.search(r"^" + "Cabernet Malbec" + r"$", item)
                has_cab_syrah = re.search(r"^" + "Cabernet Syrah" + r"$", item)
                has_cms = re.search(r"^" + "Carmenere Merlot Syrah" + r"$", item)

            
                conditions = [has_number, has_blend, has_plus, has_slash, has_period, has_ampersand, has_double_chardonay, has_cms, has_chardonay_pinot, has_chenin_chardonay, has_cabf_syrah, has_cab_malbec, has_cab_syrah ]
            
                if item != "" and len(item) < 25 and not any(conditions):
                    title_case_item = item.title()
                    if key == 'red':
                        red_varietal_set.add(title_case_item.strip())
                    if key == 'white':
                        white_varietal_set.add(title_case_item.strip())
                    if key == 'rose':
                        rose_varietal_set.add(title_case_item.strip())
                    if key == 'all':
                        all_varietal_set.add(title_case_item.strip())
   
        
        red_varietals = sorted([varietal for varietal in red_varietal_set])
        white_varietals = sorted([varietal for varietal in white_varietal_set])
        rose_varietals = sorted([varietal for varietal in rose_varietal_set])
        all_varietals = sorted([varietal for varietal in all_varietal_set])

        # import pdb
        # pdb.set_trace()
        return {"red":red_varietals, "white":white_varietals, "rose":rose_varietals, "all":all_varietals}
        
        
        # sorted_list = sorted(my_varietals)
        
        # return sorted_list
    
    
    
    
        # def get_all_varietals(self, wine_type):
        #     """Take a list of varietals and filters through each item to make sure 
        # that no elements other than text exist, as well as are certain than
        # a certain length and are not empty. Then adds to a set to remove any
        # duplicates. Then that list of varietals is returned.
        # """     
        
        # # import pdb
        # # pdb.set_trace()
        
        # varietal_list = []
        # varietal_set = set()
        # red_varietals = []
        # white_varietals = []
        # rose_varietals = []
        # all_varietals = []
        
        # if 'Red' in wine_type:
        #     red_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        
        # if 'White' in wine_type:
        #     white_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        
        # if 'Rose' in wine_type:
        #     rose_varietals = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
            
        # if (not 'Red' in wine_type and not 'White' in wine_type and not 'Rose' in wine_type) or 'All of the above' in wine_type:
        #     all_varietals = [wine.varietal.split(",") for wine in Wine.query.all()]
            
        # varietals = red_varietals + white_varietals + rose_varietals + all_varietals
            
    
        # for varietal in varietals:
        #     varietal_list = varietal_list + varietal
    
        
        
        # for item in varietal_list:
        #     has_number = re.search("\d", item)
        #     has_blend = re.search(" Blend", item)
        #     has_plus = re.search("\+", item)
        #     has_slash = re.search("/", item)
        #     has_period = re.search("\.", item)
        #     has_ampersand = re.search("&", item)
        #     has_double_chardonay = re.search(r"^" + "Chardonnay Chardonnay" + r"$", item)
        #     has_chardonay_pinot = re.search(r"^" + "Chardonnay Pinot Noir" + r"$", item)
        #     has_chenin_chardonay = re.search(r"^" + "Chenin Blanc Chardonnay" + r"$", item)
        #     has_cabf_syrah = re.search(r"^" + "Cabernet Franc Syrah" + r"$", item)
        #     has_cab_malbec = re.search(r"^" + "Cabernet Malbec" + r"$", item)
        #     has_cab_syrah = re.search(r"^" + "Cabernet Syrah" + r"$", item)
        #     has_cms = re.search(r"^" + "Carmenere Merlot Syrah" + r"$", item)

        
        #     conditions = [has_number, has_blend, has_plus, has_slash, has_period, has_ampersand, has_double_chardonay, has_cms, has_chardonay_pinot, has_chenin_chardonay, has_cabf_syrah, has_cab_malbec, has_cab_syrah ]
        
        #     if item != "" and len(item) < 25 and not any(conditions):
        #         title_case_item = item.title()
        #         varietal_set.add(title_case_item.strip())
   
        # # import pdb
        # # pdb.set_trace()
        
        # my_varietals = [varietal for varietal in varietal_set]
        
        # sorted_list = sorted(my_varietals)
        
        # return sorted_list