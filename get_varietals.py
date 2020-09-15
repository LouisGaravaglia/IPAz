
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
        ################# SETTING UP DICTS AND SETS TO PUSH TO #################
        varietal_dict = {}
        red_varietal_set = set()
        rose_varietal_set = set()
        white_varietal_set = set()
        all_varietal_set = set()
        ################# RED QUERY #################
        reds = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Red").all()]
        red_flat_list = [varietal for sublist in reds for varietal in sublist]
        varietal_dict.update({"red":red_flat_list})
        ################# WHITE QUERY #################
        whites = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="White").all()]
        white_flat_list = [varietal for sublist in whites for varietal in sublist]
        varietal_dict.update({"white":white_flat_list})
        ################# ROSE QUERY #################
        roses = [wine.varietal.split(",") for wine in Wine.query.filter_by(type="Rose").all()]
        rose_flat_list = [varietal for sublist in roses for varietal in sublist]
        varietal_dict.update({"rose":rose_flat_list})
        ################# ALL WINE QUERY #################
        alls = [wine.varietal.split(",") for wine in Wine.query.all()]
        all_flat_list = [varietal for sublist in alls for varietal in sublist]
        varietal_dict.update({"all":all_flat_list}) 
        ################# FILTERING OUT EXCEPTIONS #################
        for key,items in varietal_dict.items():
            for item in items:
                if item != "" and len(item) < 25:
                    is_redundant = re.search("\d| Blend|\+|/|\.|&|Aglianico Primitivo|Avgoustiatis Agiorgitiko|Bordeaux Blend|Bordeaux Varietals|Aligoté|Albariño|Aragones|Argonez|Babera|Aglianico Primitivo|Alfrocheiro E Jaen|Alicante B|Alicante Bouschet|Alicante Henri Bouschet|And Tinta Barroca|Arinto E Azal|Assyrtiko Athiri|Agiorgitkio|Baco Noir Reserve|Barbera D'Alba|Blind|Blueberry|Bourboulene|Chardonnay Chardonnay|Chardonnay (Fiano)|Chardonnay Pinot Noir|Chenin Blanc Chardonnay|Cabernet Franc Syrah|Cabernet Malbec|Cabernet Syrah|Carmenere Merlot Syrah|Muscat Canellii|Cabernet Sauvginon|Cab-Foch|Cab Sauvignon Blanc|Cab Sauvignon|Cabernet Franc Reserve|Cabernet Foch|Cabarnet Franc|Cabernet France|Caberent France|Cabernet Sauvingnon|Cabernet Savignon|Cabenet Sauvignon|Cabernet Merlot|Cab Franc|Canaiola Bianco|Canaiolo Nero|Caniolo|Caramenere|Carbenet|Carigan|Carignan Syrah|Carignan Syrah Grenache|Carignane Grenache|Carmenere Merlot Syrah|Carmenere Reserva|Cattarrato|Cayuga White|Cghbvf|Chardinnay|Chardonel|Chardonnay (Fiano)|Chardonnay Musque|Chateauneuf Du Pape|Clairette Blanche|Colombard Ugni Blanc|Corvina Veronese|Corvina Veroneze|Dornfender|Dry Riesling| Etc|Fernao Pires|Fiano Minutolo|French Colombard|Fruilano|Fruit|Fruit And Spiced Wine|Furmint Harslevelü Zeta|Gamay Noir|Garnacha Tintoera|Garnacha Tintorera|Garnacho Tinto|Garnatxa Cabernet|Garnaxta Negra|Gewurtztraminer|Gewurz|Gewurztraminer Riesling|Gewutztraminer|Glera (Glera)|Glera (Prosecco)|Green Apple Cassis|Grenache Blanc|Grenache Blanca|Grenache Bourboulene|Grenache Carignana|Grenache Gris|Grenache Noir|Grenache Syrah|Grenache Syrah Mourvedre|Grenache Tintorera|Grillo Chardonnay|Gsm|Hazelnut Essence|Hondarrabi Beltza|Hondarrabi Zuri|Jaen Alfrocheiro|Kekfrankos Kadarka|L'Acadia Blanc|Lambrusco Salamino|Lambrusco Sorbara|Lucy Kuhlmann|Macabeo Pinot Noir|Malbec Bonarda Syrah|Malbec Merlot|Malbec Reserva|Malvasia - Trebbiano|Malvasia Bianca|Malvasia De Candia|Malvasia Del Lazio|Malvasia Di Candia|Malvasia Di Lipari|Malvasia Istriana|Malvasia Nera|Merlot Cabernet Franc|Merlot-Cabernet|Molinara Di Marano|Monastell|Monastrell Carignan|Monastrell Tempranillo|Montepulciano D'Abruzzo|Mosacatel De Alejandria|Moscatel De Alejandria|Moscatel De Setubal|Moscatel Graudo|Moscatella|Moscato Bianco|Moscato D'Asti|Moscato Ottonel|Mourvedra|Mourvedre Syrah Grenache|Mouvedre|Nebbiolo Barbera|Old Vine Zinfandel|Palomino Pedro Ximenez|Petit Sirah Petit Verdot|Petit Verdot Merlot|Petite Sirah Syrah|Picpoul Blanc|Picpoul Gris|Pink Moscato|Pinot Pinot Noir|Portugese White|Portuguese White|Raspberry|Reisling|Riesling Feinherb|Riesling Gg|Riesling Icewine|Riesling Spaltese|Rioja - Tempranillo|Rolle Semillon|Rondinella Molinara|Rondo Regent|Rousanne And Viognier|Sangiovese Grosso|Sangiovese Grosso|Sangiovese Merlot|Sangiovese Sangiovese|Sauv Sauvignon Blanc|Sauvignn Blanc|Sauvignon Blanc Riesling|Sauvignon Blanc Semillon|Sauvingon Blanc|Savignon Blanc|Schoenburger|Schonburger|Seyval Blanc|Seyval Phoenix|Siegrebbe|Sirah Cinsault Grenache|Syrah Cabernet|Syrah Cabernet Sauvignon|Syrah Grenache|Syrah Grenache Mourvedre|Syrah Mourvedre|Syrah Rose|Syrah-Sangiovese|Tempanillo|Tempranilla|Tempranillo Blanco|Tempranillo Garnacha|Tempranillo Grenache|Tempranillo Valdepenas|Touriga Franca|Touriga Francesa|Touriga Francesca|Touriga Nacional|Touriga-Nacional|Tourigal Nacional|Trebbiano D'Abruzzo|Trebbiano Spoletino|Trebbiano Toscano|Ugni Blanc Colombard|Unknown|Viognier-Chardonnay", item)
                    if not is_redundant:
                        title_case_item = item.title()
                        if key == 'red':
                            red_varietal_set.add(title_case_item.strip())
                        if key == 'white':
                            white_varietal_set.add(title_case_item.strip())
                        if key == 'rose':
                            rose_varietal_set.add(title_case_item.strip())
                        if key == 'all':
                            all_varietal_set.add(title_case_item.strip())
        ################# SORTING LISTS AND RETURNING #################
        red_varietals = sorted([varietal for varietal in red_varietal_set])
        white_varietals = sorted([varietal for varietal in white_varietal_set])
        rose_varietals = sorted([varietal for varietal in rose_varietal_set])
        all_varietals = sorted([varietal for varietal in all_varietal_set])
        return {"red":red_varietals, "white":white_varietals, "rose":rose_varietals, "all":all_varietals}