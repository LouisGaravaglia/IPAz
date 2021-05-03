
**LINK TO FINISHED APP**

https://findwinenot.herokuapp.com/

**API**

I used the API from Quini Wine (https://quiniwine.com/app/#/toplink?linkname=data). 

**SCHEMA**

![image info](./schema/schema.png)

**FUNCTION OF SITE**

A place where users can go to find inspiration for new wines to try, as well as keep track of the wines they try with reviews and favoriting. 

**FLOW**

There is a Landing page where the user can access and utilize even if they are not logged in. It prompts the user to select a wine type (Red, White, or Rose), utilizing buttons so more than one wine type can be selected. Then a user can select various varietals based on the wine type selected, as well as how they would like to sort the results. 

The varietals provided by the API came in a string separated by commas. In order to separate them into an array and filter out as many incorrect names of varietals or typos, I used python's .split function and regex. Those were then appended to arrays based on the wines type. That's how the user can choose from standalone varietals on the landing page.

Once the user clicks the "Find my wine" button, the results are shown on a new page.

The results page has a side-bar where the user can sort by several different parameters (Wine Type, Wine Style, Rating, Vintage, Winery Alphabetical). Also, a modal will expand if the user would like to add or subtract varietals on the results page. All changes based on those selections are fulfilled using AJAX.

On the wine results lives two buttons. A favorite star and a wine review icon. If not logged-in and clicked, the user receives a flash message to sign-up or log-in in order to complete either objective.

If the user signs-up or logs-in, the navbar changes to accommodate with a Favorites route where the user can see their favorite wines. A Reviews route where they can see their reviewed wines, and a Profile route where then can see how many favorited wines and reviews they have. As well as their most recent favorite wine and top-rated wine.

**FEATURES**

HERO IMAGE - I wanted the first thing the user sees, to be a clear and concise message about what the site is all about.

WINE TYPE / VARIETALS / WINE STYLE BUTTONS - In hindsight, it may be a better UX to have a search bar in place of the buttons to select varietals, but I liked the visual rhythm and tactile-ness of the buttons. As well as, the ability to see varietals that you may not know about in case you didn't know where to begin. So, I split the difference and added a search bar to the navbar.

SEARCH BAR - A way for the user to search for a specific wine, or a catch-all like wine type or varietal. Though these results are not sortable, they can still be favorited and reviewed if logged in.

PAGINATION - I implemented pagination out of necessity since it is possible for the user to be shown all wines in the database if they do not select anything prior to hitting the "Find my wine" button. This helped speed up content loading, especially after implementing AJAX.

SORTING - The main challenge of this app that I was excited about was sorting. I wanted a way to efficiently sort database items. It proved more difficult based on various types of sorting that are allowed. I ended up using a combination of SQLalchemy queries and regex for the filters like wine type and wine style. And used javascript functions to sort the results based off of the sort parameters.

**TECH STACK**

* HTML
* CSS
* Bulma
* Javascript
* Python
* Flask
* Jinja
* PostgreSQL
* SQLalchemy
* WTForms
* Axios
* Heroku


**PERFORMANCE**

Optomized performance for Filter and Search features by indexing the PostgreSQL database for both comparsion search and partial matching. Execution time was decreased by up to 99% in some instances.

![image info](./static/images/indexing.png)

**TESTING**

Added integration and unit-testing for all routes and python functions using unittest.

Steps to run tests with VScode:

1. Open up command pallete (Command + shift + p)
2. Enter the following, Python: Run all tests
3. If VScode says that testing needs to be configured, you can set it up by clicking on the prompt and choosing unittests, and then "test_" as the filename structure.
4. Click on the "Tests" icon on the VScode sidebar.
5. Click on the "Run All Tets" icon within the "Tests" panel.
