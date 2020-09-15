import requests
from models import db, connect_db, User, Post, Wine, Favorite

# ===================================    IMPORTING WINE TO DB FUNCTION    =====================================


def import_wines():
    """Calls three functions which will make calls to the Quini API and store the
    wine in the database."""
    get_red_wines(1000, 0, 574)
    get_white_wines(1000, 0, 598)
    get_rose_wines(631, 0)  
    

# ===================================    API CALL FUNCTIONS    =====================================

def get_red_wines(amount, skip, remainder):
    """Get all top rated red wines from the API"""
    count = 0
    while count <= 7:
        count = count + 1
        if skip < 7000:
            baseURL = f"https://quiniwine.com/api/pub/wineCategory/tre/{skip}/{amount}"
        else:
            baseURL = f"https://quiniwine.com/api/pub/wineCategory/tre/{skip}/{remainder}"
        skip = skip + 1000
        headers = {'authorization': new_api_key}
        result = requests.get(f"{baseURL}", headers=headers)
        data = result.json()
        wine_array = data["items"]
        if result.status_code != 200:
            print ("There was an issue making an request for red wines to the API.")
        for wine in wine_array:
            new_wine = Wine(
                wine_id = wine["_id"],
                winery = wine["Winery"],
                country = wine["Country"],
                area = wine["Area"],
                vintage = wine["vintage"],
                varietal = wine["Varietal"],
                type = wine["Type"],
                name = wine["Name"],
                rating = wine["rating"]
            )
            db.session.add(new_wine)
            db.session.commit()
    print ("All red wines have been pulled")

def get_white_wines(amount, skip, remainder):
    """Get all top rated white wines from the API"""
    count = 0
    while count <= 4:
        count = count + 1
        if skip < 4000:
            baseURL = f"https://quiniwine.com/api/pub/wineCategory/twh/{skip}/{amount}"
        else:
            baseURL = f"https://quiniwine.com/api/pub/wineCategory/twh/{skip}/{remainder}"       
        skip = skip + 1000
        headers = {'authorization': new_api_key}
        result = requests.get(f"{baseURL}", headers=headers)
        data = result.json()
        wine_array = data["items"]
        if result.status_code != 200:
            print ("There was an issue making an request for red wines to the API.") 
        for wine in wine_array:
            new_wine = Wine(
                wine_id = wine["_id"],
                winery = wine["Winery"],
                country = wine["Country"],
                area = wine["Area"],
                vintage = wine["vintage"],
                varietal = wine["Varietal"],
                type = wine["Type"],
                name = wine["Name"],
                rating = wine["rating"]
            )
            db.session.add(new_wine)
            db.session.commit()
    print ("All white wines have been pulled")

def get_rose_wines(amount, skip):
    """Get all top rated rose wines from the API"""  
    baseURL = f"https://quiniwine.com/api/pub/wineCategory/tro/{skip}/{amount}"
    headers = {'authorization': new_api_key}
    result = requests.get(f"{baseURL}", headers=headers)
    data = result.json()
    wine_array = data["items"]
    if result.status_code != 200:
        print ("There was an issue making an request for red wines to the API.") 
    for wine in wine_array:
        new_wine = Wine(
            wine_id = wine["_id"],
            winery = wine["Winery"],
            country = wine["Country"],
            area = wine["Area"],
            vintage = wine["vintage"],
            varietal = wine["Varietal"],
            type = wine["Type"],
            name = wine["Name"],
            rating = wine["rating"]
        )
        db.session.add(new_wine)
        db.session.commit()
    print ("All rose wines have been pulled")
    
# ===================================    UNDER 10K WINES VERSION    =====================================

# @app.route('/import_wines')
# def import_wines():
#     """Calls three functions which will make calls to the Quini API and store the
#     wine in the database."""
#     get_red_wines(1000, 0, 574)
#     get_white_wines(1000, 0, 363)
#     get_rose_wines(631, 0)  
#     return render_template("import_wines.html")
    

# # ===================================    API CALL FUNCTIONS    =====================================

# def get_red_wines(amount, skip, remainder):
#     """Get all top rated red wines from the API"""
#     count = 0
#     while count <= 4:
#         count = count + 1
#         baseURL = f"https://quiniwine.com/api/pub/wineCategory/tre/{skip}/{amount}"
#         skip = skip + 1000
#         headers = {'authorization': new_api_key}
#         result = requests.get(f"{baseURL}", headers=headers)
#         data = result.json()
#         wine_array = data["items"]
#         if result.status_code != 200:
#             print ("There was an issue making an request for red wines to the API.")
#         for wine in wine_array:
#             new_wine = Wine(
#                 wine_id = wine["_id"],
#                 winery = wine["Winery"],
#                 country = wine["Country"],
#                 area = wine["Area"],
#                 vintage = wine["vintage"],
#                 varietal = wine["Varietal"],
#                 type = wine["Type"],
#                 name = wine["Name"],
#                 rating = wine["rating"]
#             )
#             db.session.add(new_wine)
#             db.session.commit()
#     print ("All red wines have been pulled")

# def get_white_wines(amount, skip, remainder):
#     """Get all top rated white wines from the API"""
#     count = 0
#     while count <= 4:
#         count = count + 1
#         if skip < 4000:
#             baseURL = f"https://quiniwine.com/api/pub/wineCategory/twh/{skip}/{amount}"
#         else:
#             baseURL = f"https://quiniwine.com/api/pub/wineCategory/twh/{skip}/{remainder}"       
#         skip = skip + 1000
#         headers = {'authorization': new_api_key}
#         result = requests.get(f"{baseURL}", headers=headers)
#         data = result.json()
#         wine_array = data["items"]
#         if result.status_code != 200:
#             print ("There was an issue making an request for red wines to the API.") 
#         for wine in wine_array:
#             new_wine = Wine(
#                 wine_id = wine["_id"],
#                 winery = wine["Winery"],
#                 country = wine["Country"],
#                 area = wine["Area"],
#                 vintage = wine["vintage"],
#                 varietal = wine["Varietal"],
#                 type = wine["Type"],
#                 name = wine["Name"],
#                 rating = wine["rating"]
#             )
#             db.session.add(new_wine)
#             db.session.commit()
#     print ("All white wines have been pulled")

# def get_rose_wines(amount, skip):
#     """Get all top rated rose wines from the API"""  
#     baseURL = f"https://quiniwine.com/api/pub/wineCategory/tro/{skip}/{amount}"
#     headers = {'authorization': new_api_key}
#     result = requests.get(f"{baseURL}", headers=headers)
#     data = result.json()
#     wine_array = data["items"]
#     if result.status_code != 200:
#         print ("There was an issue making an request for red wines to the API.") 
#     for wine in wine_array:
#         new_wine = Wine(
#             wine_id = wine["_id"],
#             winery = wine["Winery"],
#             country = wine["Country"],
#             area = wine["Area"],
#             vintage = wine["vintage"],
#             varietal = wine["Varietal"],
#             type = wine["Type"],
#             name = wine["Name"],
#             rating = wine["rating"]
#         )
#         db.session.add(new_wine)
#         db.session.commit()
#     print ("All rose wines have been pulled")