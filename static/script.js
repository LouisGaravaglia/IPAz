
/**
 * @namespace document
 */

// =================================================  GLOBAL VARIABLES  ================================================

var paginatedWine;
var unPaginatedWine;
var searchPaginatedWine;
var favs;
var reviews;

// =================================================  REFRESH HOME PAGE WITH BACKSPACE  ================================================

/**
 * This function is here so that the search parameters are cleared when the user backspaces to the landing page.
 * @event document#pageshow
 * @type {object}
 * @property {element} 
 */
window.addEventListener( "pageshow", function ( event ) {
  const address = document.location.href;
  if (!address.includes("/search") && !address.includes("/show_results") && !address.includes("/favorites") && !address.includes("/reviews") && !address.includes("/user") && !address.includes("/signup") && !address.includes("/login")) {
    var historyTraversal = event.persisted ||
          ( typeof window.performance != "undefined" && window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      window.location.reload();
    }
  }
});

// =================================================  CLEARING SESSION STORAGE / SORT BY  ================================================

/**
 * Resets the sortByArray to be empty when the user navigates back to the home page, 
 * in order to prevent the filters to be carried over from previous searches
 * @event document#ready
 * @type {object}
 * @property {element} 
 */
$(document).ready(async function() {
const address = document.location.href;
  if (!address.includes("/search") && !address.includes("/show_results") && !address.includes("/favorites") && !address.includes("/reviews") && !address.includes("/user") && !address.includes("/signup") && !address.includes("/login")) {
    const sortByArray = []
    sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    const response = await axios.get('/get_varietals')
    const redVarietals = response.data.red_varietals;
    const whiteVarietals = response.data.white_varietals;
    const roseVarietals = response.data.rose_varietals;
    const allVarietals = response.data.all_varietals;
    const selectedVarietals = response.data.selected_varietals;
    sessionStorage.setItem("redVarietals", JSON.stringify(redVarietals))
    sessionStorage.setItem("whiteVarietals", JSON.stringify(whiteVarietals))
    sessionStorage.setItem("roseVarietals", JSON.stringify(roseVarietals))
    sessionStorage.setItem("allVarietals", JSON.stringify(allVarietals))
    populateVarietals(allVarietals, selectedVarietals)
  }
});

// =================================================  POPULATE WINE RESULTS ================================================

/**
 * Function that returns an string of html elements that represent the wine card
 * which holds an indivdual wine to be added using AJAX.
 * @param {object} wine
 * @param {string} favBtn
 * @param {string} reviewBtn
 * @param {string} reviewHTML
 * @param {string} cardSize
 */
const addWineCard = function(wine, favBtn, reviewBtn, reviewHTML, cardSize) {
  const html = `<div class="column ${cardSize}">
                  <div class="has-text-centered">
                  </div>
                  <article class="message is-info">
                  <div class="message-header">
                    <p>${wine['Name']}</p>
                  </div>
                  <div class="message-body">
                    <p><strong>NAME: </strong>${wine['Name']}</p>
                    <p><strong>WINERY: </strong>${wine['Winery']}</p>
                    <p><strong>COUNTRY: </strong>${wine['Country']}</p>
                    <p><strong>AREA: </strong>${wine['Area']}</p>
                    <p><strong>VINTAGE: </strong>${wine['Vintage']}</p>
                    <p><strong>VARIETAL: </strong>${wine['Varietal']}</p>
                    <p><strong>TYPE: </strong>${wine['Type']}</p>
                    <p><strong>RATING: </strong>${wine['Rating']}</p>
                  </div>
                  <div class="columns">
                    <div class="column is-half has-text-centered mx-0 my-0">
                      <button class="button is-text favorite-button" data-id="${wine['ID']}">
                        <span class="icon">
                        ${favBtn}
                        </span>
                      </button>
                    </div>
                    <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
                    <a href="/user/review/${wine['ID']}" class="button is-text review-btn" data-id="${wine['ID']}">
                        <span class="icon review-btn">
                        ${reviewBtn}
                        </span>
                      </a>
                    </div>
                  </div>
                  ${reviewHTML}
                  </article>
                </div>`
  return html;
}

/**
 * Function that will return a string of html elements that make up the review portion
 * of the wine card
 * @param {object} wine 
 */
const addReviewHTML = function(wine) {
  const html = `<hr class="dropdown-divider"> 
                <br>
                <div class="ml-5 has-text-info-dark">
                  <p><strong>MY RATING: </strong>${wine['Post_rating']}</p>
                  <p><strong>REVIEW: </strong>${wine['Post_review']}</p>
                </div>
                <br>
                <div class="field is-grouped ml-5" id="review-delete">
                  <button class="button is-info is-outlined review-delete mb-5" data-id="${wine['ID']}">
                    <span class="review-delete">Delete</span>
                  </button>
                  <a href="/user/reviews/${wine['ID']}" class="button is-info is-outlined edit-review mb-5 ml-2">
                    <span>Edit</span>
                  </a>
                </div>`
  return html
}

/**
 * Function that will use AJAX to replace the wine cards in the DOM depending on the
 * url location address.
 * @param {object} wine_results
 * @param {array} favorites
 * @param {array} reviews
 * @param {object} fav_wines
 * @param {object} wine_reviews
 */
function populateWineResults(wine_results, favorites, reviews, fav_wines, wine_reviews) {
  const wineHtml = $("#wine-results");
  const address = document.location.href;
  wineHtml.html("");
  if (wine_results[0] == "No Results") {
    const message = `<section class="hero is-small is-light mt-6 mx-6">
                      <div class="hero-body">
                        <div class="container">
                          <h1 class="title has-text-info">
                            No wines available.
                          </h1>
                        </div>
                      </div>
                    </section>`
    wineHtml.append(message)
  } else if (address.includes("user/review")) {
    for (wine of wine_reviews) {
      if (favorites.includes(wine['ID'])) {
        const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                          <i class="fas fa-star" data-id="${wine['ID']}"></i>
                        </div>`;
        const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
        const cardSize = 'is-one-third';
        const reviewHTML = addReviewHTML(wine)
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      } else {
        const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                          <i class="far fa-star" data-id="${wine['ID']}"></i>
                        </div>`;
        const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
        const cardSize = 'is-one-third';
        const reviewHTML = addReviewHTML(wine)
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      }
    }
  } else if (address.includes("user/favorites")) {
    for (wine of fav_wines) {
      if (favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } 
    }
  } else if (address.includes("/search")) {
    for (wine of wine_results) { 
      if (favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } 
    }
  } else {
    for (wine of wine_results) { 
      if (favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" data-id="${wine['ID']}" class="myFas">
                            <i class="fas fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = `<div id="fav-box-${wine['ID']}" class="myFar">
                            <i class="far fa-star" data-id="${wine['ID']}"></i>
                          </div>`;
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } 
    }
  }
}

/**
 * Function that paginates the wine results, appends the results to the DOM, and runs conditionals
 * to see which pagination buttons need to be present based on the amount of results and which page
 * the user is currently on
 * @param {integer} numToPage 
 * @param {array} wineResults 
 * @param {array} favs 
 * @param {array} reviews 
 */
function paginateAndPopulate(numToPage, wineResults, favs, reviews){
  paginatedWine = paginate(numToPage, wineResults)
  sessionStorage.setItem("currentPage", 0)
  // ##### CONDITIONALS FOR PAGINATION NEXT AND PREVIOUS BUTTONS
  if (!$(".main-pagination-previous").hasClass("hidden")) {
    $(".main-pagination-previous").addClass("hidden")
  }
  if (wineResults.length <= numToPage && !$(".main-pagination-next").hasClass("hidden")) {
    $(".main-pagination-next").addClass("hidden")
  }
  if (wineResults.length > numToPage && $(".main-pagination-next").hasClass("hidden")) {
    $(".main-pagination-next").removeClass("hidden")
  }
  populateWineResults(paginatedWine[0], favs, reviews)
}

// =================================================  WINE TYPE / HOME PAGE  ================================================

async function makeVarietalsArray(){
  const response = await axios.get('/get_selected_varietals')
  const selectedVarietals = response.data.selected_varietals;
  const wineTypes = response.data.wine_types;
  const varietals = []
  const redVarietals = JSON.parse(sessionStorage.getItem("redVarietals"))
  const whiteVarietals = JSON.parse(sessionStorage.getItem("whiteVarietals"))
  const roseVarietals = JSON.parse(sessionStorage.getItem("roseVarietals"))
  const allVarietals = JSON.parse(sessionStorage.getItem("allVarietals"))
  if (wineTypes.includes('Red')) {
    for (item of redVarietals) varietals.push(item)
  }      
  if (wineTypes.includes('White')) {
    for (item of whiteVarietals) varietals.push(item)
  }     
  if (wineTypes.includes('Rose')) {
    for (item of roseVarietals) varietals.push(item)
  }
  if ((!wineTypes.includes('Rose') && !wineTypes.includes('White') && !wineTypes.includes('Red')) || wineTypes.includes('All of the above')) {
    for (item of allVarietals) varietals.push(item)
  }
  return [varietals, selectedVarietals]
}

/**
 * Click event that logs the wine type in the backend session.
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#wine-type").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;
  const wineType = selected_button.innerText;
  const varietalDiv = $("#varietals");
  varietalDiv.html("");
  $(selected_button).toggleClass("is-light");
  const res = await axios.get(`/wine_type/${wineType}`)
  const [varietals, selectedVarietals] = await makeVarietalsArray();
  populateVarietals(varietals.sort(), selectedVarietals)
})

// =================================================  LOADING VARIETALS / HOME PAGE ================================================

/**
 * This function loops over the varietals that need to be displayed based on the
 * wine types selected on the home page and will return a bold button
 * if it is logged as a selected_varietals
 * @param {array} varietal_array 
 * @param {array} selected_varietals 
 */
function populateVarietals(varietal_array, selected_varietals) {
  for (varietal of varietal_array) {
    const varietalDiv = $("#varietals");
    if (selected_varietals.includes(varietal)) {
      const html = `<button class="button is-info is-rounded mt-3 mb-2 mx-2 varietals">${varietal}</button>`
      varietalDiv.append(html);
    } else {
      const html = `<button class="button is-info is-light is-rounded mt-3 mb-2 mx-2 varietals">${varietal}</button>`
      varietalDiv.append(html);
    }
  }
}

// =================================================  PICKING VARIETALS / HOME PAGE  ================================================

/**
 * Click event that will bold a varietal button if the user clicks
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#varietals").on("click", ".varietals", async function(e) {
  const selected_button = e.target;
  const varietal = selected_button.innerText
  $(selected_button).toggleClass("is-light")
  await sendVarietals(varietal)
})

/**
 * Function that makes a request to the backend to log the varietal of which
 * the button the user clicked.
 * @param {string} varietal 
 */
async function sendVarietals(varietal) {
  const res = await axios.get(`/log_varietals/${varietal}`)
}

// =================================================  SORT BY / HOME PAGE ================================================

/**
 * This click event logs the sort by parameters in the backend session.
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#filter-by").on("click", ".filter-by", async function(e) {
  const selected_button = e.target;
  const filterBy = selected_button.innerText
  $(selected_button).toggleClass("is-light")
  if (sessionStorage["sortBy"]) {
    const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
    sortByArray.push(filterBy)
    sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
  } else {
    const sortByArray = [filterBy]
    sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
  }
})

// =================================================  PAGINATION / RESULTS PAGE ================================================

/**
 * When the search results page is loaded, a call to the backend is made for the wine results for the 
 * input value the user had type in. Those wines are paginated and then appended to the DOM
 */
$(document).ready(async function() {
  const address = document.location.href;
  if (address.includes("/show_results")) {
    $(".progress-bar-container").toggleClass("hidden")
    const res = await axios.get(`/show_results/json`)
    const wineResults = res.data.wines;
    favs = res.data.user_favorites;
    reviews = res.data.user_reviews;
    unPaginatedWine = wineResults;
    sessionStorage.setItem("currentPage", 0)
    const sortByFilters = JSON.parse(sessionStorage.getItem("sortBy"))
    const sortedWine = sortWine(wineResults, sortByFilters)
    const numToPage = 10;
    console.log(wineResults.length);
    paginatedWine = paginate(numToPage, sortedWine)
    if (!$(".main-pagination-previous").hasClass("hidden")) {
      $(".main-pagination-previous").addClass("hidden")
    }
    if (wineResults.length <= numToPage && !$(".main-pagination-next").hasClass("hidden")) {
      $(".main-pagination-next").addClass("hidden")
    }
    populateWineResults(paginatedWine[0], favs, reviews) 
    $(".progress-bar-container").toggleClass("hidden")
  }
});

/**
 * Click event for the next button on the pagination of the Search Results page. 
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#main-pagination").on("click", ".main-pagination-next", function() {
  const currentPage = sessionStorage.getItem("currentPage");
  const nextPage = parseInt(currentPage) + 1;
  sessionStorage.setItem("currentPage", nextPage)
  if (nextPage > 0 && $(".main-pagination-previous").hasClass("hidden")) {
    $(".main-pagination-previous").removeClass("hidden")
  }
  if (currentPage == paginatedWine.length - 2 && !$(".main-pagination-next").hasClass("hidden")) {
    $(".main-pagination-next").addClass("hidden")
  }
  populateWineResults(paginatedWine[nextPage], favs, reviews) 
})

/**
 * Click event for the previous button on the pagination of the Search Results page. 
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#main-pagination").on("click", ".main-pagination-previous", function() {
  const currentPage = sessionStorage.getItem("currentPage");
  let previousPage = parseInt(currentPage) - 1;
  if (previousPage <= 0) {
    previousPage = 0;
    if (!$(".main-pagination-previous").hasClass("hidden")) {
      $(".main-pagination-previous").addClass("hidden")
    }
  }
  if (previousPage == paginatedWine.length - 2 && $(".main-pagination-next").hasClass("hidden")) {
    $(".main-pagination-next").removeClass("hidden")
  }
  sessionStorage.setItem("currentPage", previousPage)
  populateWineResults(paginatedWine[previousPage], favs, reviews) 
})

// =================================================  FAVORITE BUTTON / RESULTS PAGE ================================================

/**
 * Appends HTML to the DOM to create a flash message to the user
 * @param {object} noUserObj 
 */    
const flashMessage = function(noUserObj) {
  const message = `<section class="hero is-small is-light">
                    <div class="hero-body">
                      <div class="container">
                        <h1 class="title has-text-grey-dark">
                          ${noUserObj.message}
                        </h1>
                      </div>
                    </div>
                  </section>`
  const flashDiv = $("#flash")
  flashDiv.html("");
  flashDiv.prepend(message)
  // ##### SCROLL BACK TO TOP OF PAGE TO RE CREATE THE SAME EFFECTS AS FLASH MESSAGING
  $(document).ready(function(){
    $(window).scrollTop(0);
  });
  function hideMessage(){
    flashDiv.html("");
  }
  setTimeout(hideMessage, 2000);
}

/**
 * Replace HTML with opposite class for fa-star element. This is necessary because due
 * to Bulma, it changes the html element during transpiling so I can't simply toggle
 * the class.
 * @param {HTMLelement} icon 
 * @param {string} wineId 
 */
function toggleStar(icon, wineId){
  if (icon.hasClass("myFas")) {
    icon.removeClass("myFas")
    icon.addClass("myFar")
    icon.html(`<i class="far fa-star" data-id="${wineId}"></i>`)
  } else {
    icon.removeClass("myFar")
    icon.addClass("myFas")
    icon.html(`<i class="fas fa-star" data-id="${wineId}"></i>`)
  }
}

/**
 * Click function that will get a hold of the wine-id data set of the wine favorited
 * and send that to log in the backend and toggle boldness of star
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#wine-results").on("click", ".favorite-button", async function(e) {
  const target = e.target;
  if (target.tagName == "BUTTON") {
    let wineId = target.children[0].children[0].children[0].dataset.id;
    const icon = $(`#fav-box-${wineId}`)
    const json = await axios.post(`/user/add_favorite/${wineId}`)
    const noUserObj = json.data
    if (Object.keys(noUserObj).length == 1) {
      flashMessage(noUserObj)
    } else {
      toggleStar(icon, wineId)
      favs = json.data.favs
      reviews = json.data.reviews
    } 
  } else if (target.tagName == "path") {
    const wineId = target.parentElement.dataset.id 
    const icon = $(`#fav-box-${wineId}`)
    const json = await axios.post(`/user/add_favorite/${wineId}`)
    const noUserObj = json.data
    if (Object.keys(noUserObj).length == 1) {
      flashMessage(noUserObj)    
    } else {
      toggleStar(icon, wineId)
      favs = json.data.favs
      reviews = json.data.reviews
    }
  } else if (target.tagName == "DIV") {
    wineId = target.firstElementChild.dataset.id;
    const icon = $(`#fav-box-${wineId}`)
    const json = await axios.post(`/user/add_favorite/${wineId}`)
    const noUserObj = json.data 
    if (Object.keys(noUserObj).length == 1) { 
      flashMessage(noUserObj)
    } else {
      toggleStar(icon, wineId)
      favs = json.data.favs
      reviews = json.data.reviews
    } 
  } else if (target.tagName == "svg") {
      const wineId = target.parentElement.parentElement.parentElement.dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
    if (Object.keys(noUserObj).length == 1) { 
      flashMessage(noUserObj)
    } else {
      toggleStar(icon, wineId)
      favs = json.data.favs
      reviews = json.data.reviews
    }
  }
})

/**
 * Clears all the flash messages after 2 seconds
 */
const clearFlash = function(){ 
  const flashDiv = $("#messageContainer");
    function hideMessage(){
      flashDiv.html("");
    }
    setTimeout(hideMessage, 2000);
}

// ##### Calls clearFlash()
$(document).ready(clearFlash)

// =================================================  DELETE BUTTON / REVIEWS PAGE  ================================================

/**
 * This function listens for a click event on the delete button on the review portion 
 * of the wine card. It then sends that associated wine ID to the backend to remove it
 * from the users reviews, and then uses AJAX to remove the wine card from the DOM, by 
 * way of populateWineResults()
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#wine-results").on("click", ".review-delete", async function(e) {
  const target = e.target;
 if (target.tagName == "BUTTON") {
    const wineId = target.dataset.id;
    const res = await axios.get(`/user/reviews/${wineId}/delete`)
    const wine_results = await axios.get(`/wine_style/""`)
    const wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    const fav_wines = res.data.fav_wines;
    const wine_reviews = res.data.wine_reviews;
    populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)
  } else if (target.tagName == "path") {
    const button = target.parentElement.parentElement.parentElement;
    const wineId = button.dataset.id;
    const res = await axios.get(`/user/reviews/${wineId}/delete`)
    const wine_results = await axios.get(`/wine_style/""`)
    const wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    const fav_wines = res.data.fav_wines;
    const wine_reviews = res.data.wine_reviews;
    populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)
  } else if (target.tagName == "SPAN") {
    const button = target.parentElement;
    const wineId = button.dataset.id;
    const res = await axios.get(`/user/reviews/${wineId}/delete`)
    const wine_results = await axios.get(`/wine_style/""`)
    const wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    const fav_wines = res.data.fav_wines;
    const wine_reviews = res.data.wine_reviews;
    populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)
  } else if (target.tagName == "svg") {
    const button = target.parentElement.parentElement;
    const wineId = button.dataset.id;
    const res = await axios.get(`/user/reviews/${wineId}/delete`)
    const wine_results = await axios.get(`/wine_style/""`)
    const wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    const fav_wines = res.data.fav_wines;
    const wine_reviews = res.data.wine_reviews;
    populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)
  }
})

// =================================================  TOGGLE OPEN SIDE BAR OPTIONS / RESULTS PAGE  ================================================

/**
 * Toggles open the wine type filters on the side bar of the results page.
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#choose-wine-type").on("click", function(e) {
  $("#wine-type-checkboxes").toggleClass("hidden")
})

/**
 * Toggles open the wine style filters on the side bar of the results page.
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#choose-wine-style").on("click", function(e) {
  $("#wine-style-checkboxes").toggleClass("hidden")
})

/**
 * Toggles open the sort by filters on the side bar of the results page.
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#choose-sort-by").on("click", function(e) {
  $("#sort-by-checkboxes").toggleClass("hidden")
})

// =================================================  WINE TYPE / RESULTS PAGE  ================================================

/**
 * Click event that will replace wine cards with AJAX based off of the wine type
 * selected by the user, by way of populateWineResults().
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#wine-type-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;
  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    $(targetInput).toggleClass("is-light")
    const res = await axios.get(`/wine_type/${filterName}`)
    const response = await axios.get(`/wine_style/""`)
    const wineResults = response.data.wine_results;
    unPaginatedWine = wineResults;
    const sortByFilters = JSON.parse(sessionStorage.getItem("sortBy"))
    const sortedWine = sortWine(wineResults, sortByFilters)
    favs = response.data.user_favorites;
    reviews = response.data.reviews;
    const numToPage = 10;
    paginateAndPopulate(numToPage, sortedWine, favs, reviews)
  }
})

// =================================================  WINE STYLE / RESULTS PAGE  ================================================

/**
 * Click event that will replace wine cards with AJAX based off of the wine style
 * selected by the user, by way of populateWineResults().
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#wine-style-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;
  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    $(targetInput).toggleClass("is-light")
    const response = await axios.get(`/wine_style/${filterName}`)
    const wineResults = response.data.wine_results;
    unPaginatedWine = wineResults;
    const sortByFilters = JSON.parse(sessionStorage.getItem("sortBy"))
    const sortedWine = sortWine(wineResults, sortByFilters)
    favs = response.data.user_favorites;
    reviews = response.data.reviews;
    const numToPage = 10;
    paginateAndPopulate(numToPage, sortedWine, favs, reviews)
  }
})

// =================================================  SORT BY / RESULTS PAGE  ================================================

/**
 * Toggles on the sorting buttons based on which filters the user has chosen
 * @event document#ready
 * @type {object}
 * @property {element}
 */
$(document).ready(async function() {
  const address = document.location.href;
  if (address.includes("/show_results")) {
    const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
    const sortBySidebar = $("#sort-by-checkboxes")
    const ratingHighestText = sortBySidebar[0].firstElementChild.firstElementChild.innerText;
    const ratingHighest = sortBySidebar[0].firstElementChild.firstElementChild.firstElementChild;
    const ratingLowestText = sortBySidebar[0].firstElementChild.nextElementSibling.firstElementChild.innerText;
    const ratingLowest = sortBySidebar[0].firstElementChild.nextElementSibling.firstElementChild.firstElementChild;
    const vintageOldestText = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.firstElementChild.innerText;
    const vintageOldest = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild;
    const vintageYoungestText = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.innerText;
    const vintageYoungest = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild;
    const wineryAlphabeticalText = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.innerText;
    const wineryAlphabetical = sortBySidebar[0].firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild;
    for (filter of sortByArray) {
      if (filter == ratingHighestText) {
        ratingHighest.classList.remove("is-light")
      } else if (filter == ratingLowestText) {
        ratingLowest.classList.remove("is-light")
      } else if (filter == vintageOldestText) {
        vintageOldest.classList.remove("is-light")
      } else if (filter == vintageYoungestText) {
        vintageYoungest.classList.remove("is-light")
      } else if (filter == wineryAlphabeticalText) {
        wineryAlphabetical.classList.remove("is-light")
      }
    }
  }
});

/**
 * Function that will sort the wine results based off of the filters in the filters array
 * @param {array} wineResults
 * @param {array} filters
 */
function sortWine(wineResults, filters) {
  for (filter of filters){
    if (filter == 'Rating (Highest)'){
      wineResults.sort(function(a,b) {
        return b.Rating - a.Rating;
      });
    }
    if (filter == 'Rating (Lowest)') {
      wineResults.sort(function(a,b) {
        return a.Rating - b.Rating;
      });
    }
    if (filter == 'Vintage (Oldest)'){
      wineResults.sort(function(a, b) {
        return a.Vintage.localeCompare(b.Vintage, undefined, {
          numeric: true,
          sensitivity: 'base'
        });
      });
    }
    if (filter == 'Vintage (Youngest)'){
      wineResults.sort(function(a, b) {
        return b.Vintage.localeCompare(a.Vintage, undefined, {
          numeric: true,
          sensitivity: 'base'
        });
      });
    }
    if (filter == 'Winery (Alphabetically)'){
      wineResults.sort(function(a,b) {
        let x = a.Winery.toLowerCase();
        let y = b.Winery.toLowerCase();
        return x < y ? -1 : x > y ? 1 : 0;
      });
    }
  }
  return wineResults
}

/**
 * Adds the chosen sort by filter to sessionStorage
 * @param {HTMLelement} target 
 */
function setSortBy(target){
  const filterBy = target.nextSibling.data;
  const targetInput = target.parentElement.firstElementChild;
  $(targetInput).toggleClass("is-light")
  if (sessionStorage["sortBy"]) {
    const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
    if (sortByArray.includes(filterBy)){
      const index = sortByArray.indexOf(filterBy)
      sortByArray.splice(index, 1)
      sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    } else {
      sortByArray.push(filterBy)
      sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    }
  } else {
    const sortByArray = [filterBy]
    sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
  }
}

/**
 * Certain sortBy filters are opposites. Rating Highest vs Rating lowest, etc. If one is 
 * selected, the other is then deselected with this function
 * @param {HTMLelement} target
 */
function toggleOpposites(target){
  const filterBy = target.nextSibling.data;
  if (filterBy == 'Rating (Highest)') {
    const ratingLowest = target.nextSibling.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild; 
    if (!ratingLowest.classList.contains("is-light")) {
        ratingLowest.classList.add("is-light")
        const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
        const index = sortByArray.indexOf("Rating (Lowest)")
        sortByArray.splice(index, 1)
        sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    }
  } else if (filterBy == 'Rating (Lowest)') {
    const ratingHighest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
    if (!ratingHighest.classList.contains("is-light")) {
      ratingHighest.classList.add("is-light")
      const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
      const index = sortByArray.indexOf('Rating (Highest)')
      sortByArray.splice(index, 1)
      sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    }
  } else if (filterBy == 'Vintage (Oldest)') {
    const vintageYoungest = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
    if (!vintageYoungest.classList.contains("is-light")) {
      vintageYoungest.classList.add("is-light")
      const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
      const index = sortByArray.indexOf('Vintage (Youngest)')
      sortByArray.splice(index, 1)
      sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    }
  } else if (filterBy == 'Vintage (Youngest)') {
    const vintageOldest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
    if (!vintageOldest.classList.contains("is-light")) {
      vintageOldest.classList.add("is-light")
      const sortByArray = JSON.parse(sessionStorage.getItem("sortBy"))
      const index = sortByArray.indexOf('Vintage (Oldest)')
      sortByArray.splice(index, 1)
      sessionStorage.setItem("sortBy", JSON.stringify(sortByArray))
    }
  } 
}

/**
 * Click event that will replace wine cards with AJAX based off of the sort by options
 * selected by the user, by way of populateWineResults().
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#sort-by-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;
  if (target.tagName == "INPUT") {
    setSortBy(target)
    toggleOpposites(target)
    const sortFilters = JSON.parse(sessionStorage.getItem("sortBy"))
    const wineResults = unPaginatedWine;
    const numToPage = 10;
    const sortedWine = sortWine(wineResults, sortFilters)
    console.log(wineResults.length);
    paginateAndPopulate(numToPage, sortedWine, favs, reviews)
  }
})

// =================================================  LOADING VARIETALS / RESULTS PAGE ================================================

/**
 * Click event that will load the varietal buttons by way of makeModal()
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#choose-varietals").on("click", async function() {
  const varietalDiv = $("#varietals-modal")
  varietalDiv.html("")
  const [varietals, selectedVarietals] = await makeVarietalsArray();
  makeModal(varietals, selectedVarietals)
  const modal = $(".modal");
  modal.toggleClass("is-active")
})

/**
 * Adds a button to represent the varietal to the modal
 * @param {array} varietal_array
 * @param {array} selected_varietals
 */
function makeModal(varietal_array, selected_varietals) {
  const varietalDiv = $("#varietals-modal")
  for (varietal of varietal_array) {
    if (selected_varietals.includes(varietal)) {
      const html = `<button class="button is-info is-rounded mt-3 mb-2 mx-2 wine-type varietals">${varietal}</button>`
      varietalDiv.append(html);
    } else {
      const html = `<button class="button is-info is-light is-rounded mt-3 mb-2 mx-2 wine-type varietals">${varietal}</button>`
      varietalDiv.append(html);
    }
  }
}

// =================================================  PICKING VARIETALS / RESULTS PAGE  ================================================

/**
 * Click event that will replace the buttons with the bolded buttons when clicked
 * and the send that varietal name to the backend to keep track of in session
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#varietals-modal").on("click", ".varietals", async function(e) {
  const target = e.target;
  const targetName = target.innerText;
  target.classList.toggle("is-light")
  await sendVarietals(targetName)
})

/**
 * Populates the wine results page with wine cards based off of the varietals
 * that had just been selected
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#modal").on("click", ".toggle-off", async function() {
  const modal = $(".modal");
  const response = await axios.get(`/wine_style/""`)
  modal.removeClass("is-active")
  const wineResults = response.data.wine_results;
  unPaginatedWine = wineResults;
  const sortByFilters = JSON.parse(sessionStorage.getItem("sortBy"))
  const sortedWine = sortWine(wineResults, sortByFilters)
  const numToPage = 10;
  paginateAndPopulate(numToPage, sortedWine, favs, reviews)
})

// =================================================  SEARCH  ================================================

/**
 * Click event that will trigger a enter button keyboard event when the user
 * clicks the search icon
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#search-form").on("click", ".magnify-glass", function() {
    const event = new KeyboardEvent("keypress", {
      view: window,
      keyCode: 13,
      bubbles: true,
      cancelable: true
    });
  document.querySelector("input").dispatchEvent(event);
})

/**
 * Click event that will grab the value of the search input and redirect
 * the user to the search results page
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#search-bar-box").on("click", ".search-bar", function() {
  const searchValue = $("#search-bar").val()
  sessionStorage.setItem('searchValue', searchValue);
  window.location.assign("https://wine-not-app.herokuapp.com//search");
})

// =================================================  PAGINATION  / SEARCH PAGE ================================================

/**
 * Creates arrays within an array to paginate the wine results in the amount deemed necessary
 * per page, which is what numToPage represents
 * @param {integer} numToPage
 * @param {array} wineResults
 */
function paginate(numToPage, wineResults){
  const paginatedWine = []
  let a, b
  for (a = 0; a < wineResults.length; a += numToPage) {
    const wineGroup = [];
    for (b = 0; b <= numToPage - 1; b++) {
      wineGroup.push(wineResults[b+a])
      if ( a+b >= wineResults.length - 1) {
          break
      }
    }
    paginatedWine.push(wineGroup)
  }
  return paginatedWine
}

/**
 * When the search results page is loaded, a call to the backend is made for the wine results for the 
 * input value the user had type in. Those wines are paginated and then appended to the DOM
 */
$(document).ready(async function() {
  const address = document.location.href;
  if (address.includes("/search")) {
    $(".progress-bar-container").toggleClass("hidden")
    const searchValue = sessionStorage.getItem('searchValue');
    const res = await axios.get(`/search/${searchValue}`)
    const wineResults = res.data.wine_results;
    favs = res.data.favs;
    reviews = res.data.reviews;
    if (wineResults.length == 0) {
      const message = {"message":"No results"}
      flashMessage(message)
      $(".progress-bar-container").toggleClass("hidden")
    } else {
      searchPaginatedWine = paginate(9, wineResults)
      sessionStorage.setItem("searchCurrentPage", 0)
      $(".search-pagination-previous").toggleClass("hidden")
      if (searchPaginatedWine.length == 1) {
        $(".search-pagination-next").toggleClass("hidden")
      }
      populateWineResults(searchPaginatedWine[0], favs, reviews) 
      $(".progress-bar-container").toggleClass("hidden")
    }
  }
});

/**
 * Click event for the next button on the pagination of the Search Results page. 
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#search-pagination").on("click", ".search-pagination-next", function() {
  const currentPage = sessionStorage.getItem("searchCurrentPage");
  const nextPage = parseInt(currentPage) + 1;
  sessionStorage.setItem("searchCurrentPage", nextPage)
  if (currentPage == 0) {
    $(".search-pagination-previous").toggleClass("hidden")
  }
  if (currentPage == searchPaginatedWine.length - 2) {
    $(".search-pagination-next").toggleClass("hidden")
  }
  populateWineResults(searchPaginatedWine[nextPage], favs, reviews)
})

/**
 * Click event for the previous button on the pagination of the Search Results page. 
 * @event document#click
 * @type {object}
 * @property {element}
 */
$("#search-pagination").on("click", ".search-pagination-previous", function() {
  const currentPage = sessionStorage.getItem("searchCurrentPage");
  let previousPage = parseInt(currentPage) - 1;
  if (previousPage <= 0) {
    previousPage = 0;
    $(".search-pagination-previous").toggleClass("hidden")
  }
  if (previousPage == searchPaginatedWine.length - 2) {
    $(".search-pagination-next").toggleClass("hidden")
  }
  sessionStorage.setItem("searchCurrentPage", previousPage)
  populateWineResults(searchPaginatedWine[previousPage], favs, reviews) 
})

// =================================================  NAVBAR  ================================================

/**
 * Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
 * @event document#click
 * @type {object}
 * @property {element}
 */
$(document).ready(
  function() {
  $(".navbar-burger").click(function() {
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
  });
});