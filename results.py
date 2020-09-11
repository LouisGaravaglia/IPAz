
from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify, g
from sqlalchemy import desc
import re
from get_varietals import Varietals
from models import db, connect_db, User, Post, Wine, Favorite

class WineResults():

    def wine_results(self, varietals, wine_style, wine_type_list):
        """Returns wine results based of user selected varietals,
        wine style, and wine type.
        """
        varietal_cls = Varietals()
        wine_results = []
        for wine_type in wine_type_list:
            ################# GETTING RESULTS FOR RED WINE TYPE #################
            if wine_type == 'Red':
                results = []
                if varietals == ['All']:
                    results = Wine.query.filter(Wine.type == 'Red').all()
                else:
                    for varietal in varietals:
                        db_results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'Red'))).all()
                        results.extend(db_results)
                for style in wine_style:
                    if style == 'Single Varietals':
                        for result in results:
                            if re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    elif style == 'Blends':
                        for result in results:
                            if not re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    else:
                        for result in results:
                            rating = round(result.rating, 2)
                            wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                            wine_results.append(wine)
            ################# GETTING RESULTS FOR WHITE WINE TYPE #################
            elif wine_type == 'White':
                results = []
                if varietals == ['All']:
                    results = Wine.query.filter(Wine.type == 'White').all()
                else:
                    for varietal in varietals:
                        db_results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'White'))).all()
                        results.extend(db_results)
                for style in wine_style:
                    if style == 'Single Varietals':
                        for result in results:
                            if re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    elif style == 'Blends':
                        for result in results:
                            if not re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    else:
                        for result in results:
                            rating = round(result.rating, 2)
                            wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                            wine_results.append(wine)
            ################# GETTING RESULTS FOR ROSE WINE TYPE #################
            elif wine_type == 'Rose':
                results = []
                if varietals == ['All']:
                    results = Wine.query.filter(Wine.type == 'Red').all()
                else:
                    for varietal in varietals:
                        db_results = Wine.query.filter((Wine.varietal.ilike(f'%{varietal}%') & (Wine.type == 'Rose'))).all()
                        results.extend(db_results)
                for style in wine_style:
                    if style == 'Single Varietals':
                        for result in results:
                            if re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    elif style == 'Blends':
                        for result in results:
                            if not re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    else:
                        for result in results:
                            rating = round(result.rating, 2)
                            wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                            wine_results.append(wine)
            ################# GETTING RESULTS FOR ALL WINE TYPES #################
            elif wine_type == 'All of the above':
                results = []
                if varietals == ['All']:
                    results = Wine.query.all()
                else:
                    for varietal in varietals:
                        db_results = Wine.query.filter(Wine.varietal.ilike(f'%{varietal}%')).all()
                        results.extend(db_results)
                for style in wine_style:
                    if style == 'Single Varietals':
                        for result in results:
                            if re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    elif style == 'Blends':
                        for result in results:
                            if not re.search(r"^" + varietal + r"$", result.varietal):
                                rating = round(result.rating, 2)
                                wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                                wine_results.append(wine)
                    else:
                        for result in results:
                            rating = round(result.rating, 2)
                            wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
                            wine_results.append(wine)
        ################# REMOVING DUPLICATES #################
        wine_results = [dict(s) for s in set(frozenset(d.items()) for d in wine_results)]
        return wine_results

    def search_results(self, search_term):
        """Returns wine based off what keyword the user types into the search bar."""
        results = []
        wine_results = []
        ################# QUERIES #################
        winery_results = Wine.query.filter((Wine.winery.ilike(f'%{search_term}%'))).all()
        country_results = Wine.query.filter((Wine.country.ilike(f'%{search_term}%'))).all()
        area_results = Wine.query.filter((Wine.area.ilike(f'%{search_term}%'))).all()
        vintage_results = Wine.query.filter((Wine.vintage.ilike(f'%{search_term}%'))).all()
        varietal_results = Wine.query.filter((Wine.varietal.ilike(f'%{search_term}%'))).all()
        type_results = Wine.query.filter((Wine.type.ilike(f'%{search_term}%'))).all()
        name_results = Wine.query.filter((Wine.name.ilike(f'%{search_term}%'))).all()
        ################# COMBINE RESULTS #################
        results = results + winery_results + country_results + area_results + vintage_results + varietal_results + type_results + name_results
        ################# TURN RESULT INTO OBJECT #################
        for result in results:
            rating = round(result.rating, 2)
            wine = {'ID':result.id, 'Rating':rating, 'Winery':result.winery, 'Country':result.country, 'Vintage':result.vintage, 'Area':result.area, 'Varietal':result.varietal, 'Type':result.type, 'Name':result.name}
            wine_results.append(wine)
        ################# REMOVE DUPLICATES #################
        wine_results = [dict(s) for s in set(frozenset(d.items()) for d in wine_results)]
        return wine_results