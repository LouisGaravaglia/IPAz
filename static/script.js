
/**
 * @namespace document
 */



/**
 * This function is here so that the user favorites get updated in the show_results route if the user
 * hits back from the favorties route after unfavoriting a wine.
 * @event document#click
 * @type {object}
 * @property {element} 
 */
window.addEventListener( "pageshow", function ( event ) {
  const address = document.location.href;

  // if (address.includes("show_results") ) {
      var historyTraversal = event.persisted || 
            ( typeof window.performance != "undefined" && window.performance.navigation.type === 2 );
      if ( historyTraversal ) {
        window.location.reload();
      }
  // }
});

// =================================================  WINE TYPE / HOME PAGE  ================================================


/**
 * Click event that logs the wine type in the backend session.
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#wine-type").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;

  // selected_button.classList.toggle("is-focused")
  $(selected_button).toggleClass("is-light")

  wine_type = selected_button.innerText
  varietalDiv = $("#varietals")
  varietalDiv.html("")

  await sendWineType(wine_type)
  
  const items = await axios.get('/get_varietals')
  varietal_array = items.data.varietals;
  selected_varietals = items.data.selected_varietals;

  populateVarietals(varietal_array, selected_varietals)
  
})

/**
 * Function that sends wine type to the backend to log into session.
 * @param {*} wine_type 
 */
async function sendWineType(wine_type) {
  const res = await axios.get(`/wine_type/${wine_type}`)
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

  // selected_button.classList.toggle("is-focused")
  $(selected_button).toggleClass("is-light")

  filterBy = selected_button.innerText
  
  await sendSortBy(filterBy)
  
})

/**
 * function that sends the sort by parameter to backend to add to session.
 * @param {string} filterBy 
 */
async function sendSortBy(filterBy) {
  const res = await axios.get(`/sort_by/${filterBy}`)
}

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
  if (selected_varietals.includes(varietal)) {
    html = `<button class="button is-info is-rounded mt-3 mb-2 mx-2 varietals">${varietal}</button>`
    varietalDiv.append(html);
  } else {
    html = `<button class="button is-info is-light is-rounded mt-3 mb-2 mx-2 varietals">${varietal}</button>`
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

  // selected_button.classList.toggle("is-focused")
  $(selected_button).toggleClass("is-light")

  varietal = selected_button.innerText
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

  html = `<hr class="dropdown-divider"> 
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
  wineHtml = $("#wine-results")
  wineHtml.html("")
  const address = document.location.href;


  if (wine_results[0] == "No Results") {
    
    message = `<section class="hero is-small is-light mt-6 mx-6">
  <div class="hero-body">
    <div class="container">
      <h1 class="title has-text-info">
        No wines available.
      </h1>
    </div>
  </div>
</section>`
    // const html = '<h3 class="title is-3 has-text-centered mt-6">No wines available.</h3>'
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



// =================================================  PAGINATION / RESULTS PAGE ================================================


// /**
//  * Click event that will grab the value of the search input and redirect
//  * the user to the search results page
//  * @event document#click
//  * @type {object}
//  * @property {element} 
//  */
// $("#find-wine-btn").on("click", ".results-arrow", function() {
//   searchValue = $("#search-bar").val()
//   sessionStorage.setItem('searchValue', searchValue);
//   window.location.assign("http://127.0.0.1:5000/search");
// })


var paginatedWine;


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
      const favs = res.data.user_favorites;
      const reviews = res.data.user_reviews;
      const numToPage = 10;
      console.log(wineResults);
      
      // if (wineResults.length == 0) {
      //   const message = {"message":"No results"}
      //   flashMessage(message)
      // }

      paginatedWine = paginate(numToPage, wineResults)
      // console.log(paginatedWine);
  
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))
      sessionStorage.setItem("currentPage", 0)

      

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
  const favs = JSON.parse(sessionStorage.getItem("favs"));
  const reviews = JSON.parse(sessionStorage.getItem("reviews"));
  const nextPage = parseInt(currentPage) + 1;
  sessionStorage.setItem("currentPage", nextPage)
  console.log(paginatedWine.length);

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
  const favs = JSON.parse(sessionStorage.getItem("favs"));
  const reviews = JSON.parse(sessionStorage.getItem("reviews"));
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
  message = `<section class="hero is-small is-light">
    <div class="hero-body">
      <div class="container">
        <h1 class="title has-text-grey-dark">
          ${noUserObj.message}
        </h1>
      </div>
    </div>
  </section>`

  flashDiv = $("#flash")
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
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))

    
    if (Object.keys(noUserObj).length == 1) {

      flashMessage(noUserObj)
  
    } else {

      toggleStar(icon, wineId)

    } 

  } else if (target.tagName == "path") {
    const wineId = target.parentElement.dataset.id 
    const icon = $(`#fav-box-${wineId}`)
    const json = await axios.post(`/user/add_favorite/${wineId}`)
    const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))


    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)
       
    } else {
      
      toggleStar(icon, wineId)

    }

  } else if (target.tagName == "DIV") {
    // console.log(target.firstChild.dataset.id);
    wineId = target.firstElementChild.dataset.id;
    const icon = $(`#fav-box-${wineId}`)
    const json = await axios.post(`/user/add_favorite/${wineId}`)
    const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))
console.log(favs);

    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)

    } else {
      
      toggleStar(icon, wineId)
    } 

  } else if (target.tagName == "svg") {
      const wineId = target.parentElement.parentElement.parentElement.dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))


    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)

    } else {
      
      toggleStar(icon, wineId)
    }
  }
})



/**
 * Clears all the flash messages after 2 seconds
 */
const clearFlash = function(){ 
  flashDiv = $("#messageContainer");
    function hideMessage(){
      flashDiv.html("");
    }
    setTimeout(hideMessage, 2000);
}

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
      let wineId = target.dataset.id;
      const res = await axios.get(`/user/reviews/${wineId}/delete`)
      const wine_results = await axios.get(`/wine_style/""`)
      wines = wine_results.data.wine_results;
      favs = wine_results.data.user_favorites;
      reviews = wine_results.data.reviews;
      fav_wines = res.data.fav_wines;
      wine_reviews = res.data.wine_reviews;
      populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)

    } else if (target.tagName == "path") {
      const button = target.parentElement.parentElement.parentElement;
      let wineId = button.dataset.id;
      const res = await axios.get(`/user/reviews/${wineId}/delete`)
      const wine_results = await axios.get(`/wine_style/""`)
      wines = wine_results.data.wine_results;
      favs = wine_results.data.user_favorites;
      reviews = wine_results.data.reviews;
      fav_wines = res.data.fav_wines;
      wine_reviews = res.data.wine_reviews;
      populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)

    } else if (target.tagName == "SPAN") {
      const button = target.parentElement;
      let wineId = button.dataset.id;
      const res = await axios.get(`/user/reviews/${wineId}/delete`)
      const wine_results = await axios.get(`/wine_style/""`)
      wines = wine_results.data.wine_results;
      favs = wine_results.data.user_favorites;
      reviews = wine_results.data.reviews;
      fav_wines = res.data.fav_wines;
      wine_reviews = res.data.wine_reviews;
      populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)

    } else if (target.tagName == "svg") {
      const button = target.parentElement.parentElement;
      let wineId = button.dataset.id;
      const res = await axios.get(`/user/reviews/${wineId}/delete`)
      const wine_results = await axios.get(`/wine_style/""`)
      wines = wine_results.data.wine_results;
      favs = wine_results.data.user_favorites;
      reviews = wine_results.data.reviews;
      fav_wines = res.data.fav_wines;
      wine_reviews = res.data.wine_reviews;
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
// =================================================  CLICK EVENT FOR WINE OPTIONS / RESULTS PAGE  ================================================


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
    // $(targetInput).toggleClass("is-focused")
    $(targetInput).toggleClass("is-light")
    $(".progress-bar-container").toggleClass("hidden")
    const res = await axios.get(`/wine_type/${filterName}`)
    const response = await axios.get(`/wine_style/""`)
    $(".progress-bar-container").toggleClass("hidden")
    wineResults = response.data.wine_results;
    favs = response.data.user_favorites;
    reviews = response.data.reviews;
    const numToPage = 10;
    console.log(wineResults);

    paginatedWine = paginate(numToPage, wineResults)
    // console.log(paginatedWine);

    sessionStorage.setItem("favs", JSON.stringify(favs))
    sessionStorage.setItem("reviews", JSON.stringify(reviews))
    sessionStorage.setItem("currentPage", 0)

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
})

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
    // $(targetInput).toggleClass("is-focused")
    $(targetInput).toggleClass("is-light")
    $(".progress-bar-container").toggleClass("hidden")
    const wine_results = await axios.get(`/wine_style/${filterName}`)
    $(".progress-bar-container").toggleClass("hidden")
    wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    populateWineResults(wines, favs, reviews)
  }
})

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
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    // $(targetInput).toggleClass("is-focused")
    $(targetInput).toggleClass("is-light")
    $(".progress-bar-container").toggleClass("hidden")
    const res = await axios.get(`/sort_by/${filterName}`)
    const response = await axios.get(`/wine_style/""`)
    $(".progress-bar-container").toggleClass("hidden")
    wines = response.data.wine_results;
    favs = response.data.user_favorites;
    reviews = response.data.reviews;
    populateWineResults(wines, favs, reviews)

  }

})

// =================================================  LOADING VARIETALS / RESULTS PAGE ================================================


/**
 * Opens the modal filled with varietals when the user clicks the varietals button
 * on the side bar 
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#varietals-button").on("click", async function() {
  varietalDiv = $("#varietals")
  varietalDiv.html("")
  const items = await axios.get('/get_varietals')
  varietal_array = items.data.varietals;
  selected_varietals = items.data.selected_varietals;
  makeModal(varietal_array, selected_varietals)
  modal = $(".modal");
  modal.toggleClass("is-active")
})



/**
 * Adds a button to represent the varietal to the modal
 * @param {array} varietal_array 
 * @param {array} selected_varietals 
 */
function makeModal(varietal_array, selected_varietals) {

for (varietal of varietal_array) {
  if (selected_varietals.includes(varietal)) {
    html = `<button class="button is-info is-rounded mt-3 mb-2 mx-2 wine-type varietals">${varietal}</button>`
    varietalDiv.append(html);
  } else {
    html = `<button class="button is-info is-light is-rounded mt-3 mb-2 mx-2 wine-type varietals">${varietal}</button>`
    varietalDiv.append(html);
  }

}
}


// =================================================  PICKING VARIETALS / RESULTS PAGE  ================================================



/**
 * Click event that will load the varietal buttons by way of makeModal()
 * @event document#click
 * @type {object}
 * @property {element} 
 */
$("#choose-varietals").on("click", async function() {
  varietalDiv = $("#varietals-modal")
  varietalDiv.html("")
  const items = await axios.get('/get_varietals')
  varietal_array = items.data.varietals;
  selected_varietals = items.data.selected_varietals;
  makeModal(varietal_array, selected_varietals)
  modal = $(".modal");
  modal.toggleClass("is-active")
})


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

  // target.classList.toggle("is-focused")
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
  modal = $(".modal");
  modal.toggleClass("is-active")
$(".progress-bar-container").toggleClass("hidden")
  const wine_results = await axios.get(`/wine_style/""`)
  $(".progress-bar-container").toggleClass("hidden")
  wines = wine_results.data.wine_results;
  favs = wine_results.data.user_favorites;
  reviews = wine_results.data.reviews;
  populateWineResults(wines, favs, reviews)

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
  searchValue = $("#search-bar").val()
  sessionStorage.setItem('searchValue', searchValue);
  window.location.assign("http://127.0.0.1:5000/search");
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



var searchPaginatedWine;


/**
 * When the search results page is loaded, a call to the backend is made for the wine results for the 
 * input value the user had type in. Those wines are paginated and then appended to the DOM
 */
$(document).ready(async function() {
  const address = document.location.href;

  if (address.includes("/search")) {
      const searchValue = sessionStorage.getItem('searchValue');
      const res = await axios.get(`/search/${searchValue}`)
      const wineResults = res.data.wine_results;
      const favs = res.data.favs;
      const reviews = res.data.reviews;
      
      if (wineResults.length == 0) {
        const message = {"message":"No results"}
        flashMessage(message)
      }

      searchPaginatedWine = paginate(9, wineResults)
  
      sessionStorage.setItem("favs", JSON.stringify(favs))
      sessionStorage.setItem("reviews", JSON.stringify(reviews))
      sessionStorage.setItem("searchCurrentPage", 0)

      $(".search-pagination-previous").toggleClass("hidden")

      if (searchPaginatedWine.length == 1) {
        $(".search-pagination-next").toggleClass("hidden")
      }
  
      populateWineResults(searchPaginatedWine[0], favs, reviews) 
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
  const favs = JSON.parse(sessionStorage.getItem("favs"));
  const reviews = JSON.parse(sessionStorage.getItem("reviews"));
  const nextPage = parseInt(currentPage) + 1;
  sessionStorage.setItem("searchCurrentPage", nextPage)
  console.log(searchPaginatedWine.length);

  if (currentPage == 0) {
    $(".search-pagination-previous").toggleClass("hidden")
  }

  if (currentPage == searchPaginatedWine.length - 2) {
    $(".search-pagination-next").toggleClass("hidden")
    console.log("i'm at the end");
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
  const favs = JSON.parse(sessionStorage.getItem("favs"));
  const reviews = JSON.parse(sessionStorage.getItem("reviews"));
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



// =================================================  FAVORITE BUTTON / SEARCH RESULTS PAGE  ================================================



/**
 * Click event for the favorite star on the search result wine cards to then call
 * logSearchFav() to eventually replace the wine card with the bolded favorite star
 * @event document#click
 * @type {object}
 * @property {element} 
 */
 $("#search-results").on("click", ".favorite-button", async function(e) {

    const target = e.target;

    if (target.tagName == "BUTTON") {
      let wineId = target.children[0].children[0].dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", favs)
      sessionStorage.setItem("reviews", reviews)

    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)
       
    } else {
      
      toggleStar(icon, wineId)

    }

    } else if (target.tagName == "path") {
    let wineId = target.parentElement.dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", favs)
      sessionStorage.setItem("reviews", reviews)

    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)
       
    } else {
      
      toggleStar(icon, wineId)

    };

    } else if (target.tagName == "SPAN") {
      let wineId = target.parentElement.parentElement.dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", favs)
      sessionStorage.setItem("reviews", reviews)

    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)
       
    } else {
      
      toggleStar(icon, wineId)

    }

    } else if (target.tagName == "svg") {
      let wineId = target.dataset.id;
      const icon = $(`#fav-box-${wineId}`)
      const json = await axios.post(`/user/add_favorite/${wineId}`)
      const noUserObj = json.data
      const favs = json.data.favs
      const reviews = json.data.reviews
      sessionStorage.setItem("favs", favs)
      sessionStorage.setItem("reviews", reviews)

    if (Object.keys(noUserObj).length == 1) {
      
      flashMessage(noUserObj)
       
    } else {
      
      toggleStar(icon, wineId)

    }

    }

  })



// =================================================  EVENTUALLY DELETE  ================================================


// $("#search-bar-box").on("click", ".search-bar", async function() {

//   const searchValue = $("#search-bar").val()
//   // console.log(searchValue);

//   window.location = "http://127.0.0.1:5000/search"

//   const res = await axios.get(`/search/${searchValue}`)
//   paginatedWines = res.data.paginated;
//   favs = res.data.favs;
//   reviews = res.data.reviews;

//   // window.location.assign("http://127.0.0.1:5000/search");
//   // window.location = "http://127.0.0.1:5000/search"

//   populateWineResults(paginatedWines[0], favs, reviews) 

 
// })

//   if (wine_results[0] == "No Results") {
    
//     message = `<section class="hero is-small is-light mt-6 mx-6">
//   <div class="hero-body">
//     <div class="container">
//       <h1 class="title has-text-info">
//         No wines available.
//       </h1>
//     </div>
//   </div>
// </section>`
//     // const html = '<h3 class="title is-3 has-text-centered mt-6">No wines available.</h3>'
//     wineHtml.append(message)

//   } else {

//     for (wine of wine_results) { 

//     if (favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
//         const favBtn = '<i class="fas fa-star"></i>';
//         const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
//         const reviewHTML = "";
//         const cardSize = 'is-one-third';
//         const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
//         wineHtml.append(html)
//       } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
//           const favBtn = '<i class="fas fa-star"></i>';
//           const reviewBtn = '<i class="far fa-edit review-btn"></i>';
//           const reviewHTML = "";
//           const cardSize = 'is-one-third';
//           const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
//           wineHtml.append(html)
//       } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
//           const favBtn = '<i class="far fa-star"></i>';
//           const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
//           const reviewHTML = "";
//           const cardSize = 'is-one-third';
//           const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
//           wineHtml.append(html)
//       } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
//           const favBtn = '<i class="far fa-star"></i>';
//           const reviewBtn = '<i class="far fa-edit review-btn"></i>';
//           const reviewHTML = "";
//           const cardSize = 'is-one-third';
//           const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
//           wineHtml.append(html)
//       } 

//     }

//   }

// }


// /**
//  * logs the wine id of the wine that the user favorited and then uses AJAX to re-populate
//  * the wine cards to the DOM with the wine that was just faved now showing a bold star
//  * @param {integer} wineId 
//  */
// const logSearchFav = async function(wineId) {
  
//   const json = await axios.post(`/user/add_favorite/${wineId}`)
//   noUserObj = json.data

//   // ##### CONDITIONAL TO CHECK TO SEE IF USER IS LOGGED IN IF NOT AN ERROR MESSAGE APPEARS #####
//   if (Object.keys(noUserObj).length == 1) {
    
// message = `<section class="hero is-small is-light">
//   <div class="hero-body">
//     <div class="container">
//       <h1 class="title has-text-grey-dark">
//         ${noUserObj.message}
//       </h1>
//     </div>
//   </div>
// </section>`

//     flashDiv = $("#flash")
//     flashDiv.html("");
//     flashDiv.prepend(message)
//     function hideMessage(){
//       flashDiv.html("");
//     }
//     setTimeout(hideMessage, 2000);

//   } else {
//       $(".progress-bar-container").toggleClass("hidden")
//       const wine_results = await axios.get(`/search/results`)
//       $(".progress-bar-container").toggleClass("hidden")
//       wines = wine_results.data.wine_results;
//       favs = wine_results.data.favs;
//       reviews = wine_results.data.reviews;
//       populateSearchResults(wines, favs, reviews)
//   }
// }


// /**
//  * Click event for the favorite star on the search result wine cards to then call
//  * logSearchFav() to eventually replace the wine card with the bolded favorite star
//  * @event document#click
//  * @type {object}
//  * @property {element} 
//  */
//  $("#search-results").on("click", ".favorite-button", async function(e) {

//     const target = e.target;

//     if (target.tagName == "BUTTON") {
//       let wineId = target.dataset.id;
//       logSearchFav(wineId);

//     } else if (target.tagName == "path") {
//       const button = target.parentElement.parentElement.parentElement;
//       let wineId = button.dataset.id;
//       logSearchFav(wineId);

//     } else if (target.tagName == "SPAN") {
//       const button = target.parentElement;
//       let wineId = button.dataset.id;
//       logSearchFav(wineId);

//     } else if (target.tagName == "svg") {
//       const button = target.parentElement.parentElement;
//       let wineId = button.dataset.id;
//       logSearchFav(wineId);

//     }

//   })

// var currentPage = 0;

// $("#search-pagination").on("click", ".pagination-next", async function() {
//   currentPage += 1;
//   // alert("haha")
//   const res = await axios.get(`/search/${currentPage}`)
  
//   // console.log(res);
// })

// $("#search-pagination").on("click", ".pagination-previous", async function(currentPage) {
//   if (currentPage >= 1) currentPage -= 1;
//   const res = await axios.get(`/search/${currentPage}`)
// })

// window.addEventListener("beforeunload", function(event) { 

// currentPage = 0;

//  });

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

// =================================================  PROGRESS BAR ================================================

// $(".results-button").on("click", function(){
//   // $(".progress-bar-container").toggleClass("hidden")
  
// })

// jQuery(document).ready(function() {
//     jQuery('.progress-bar-container').fadeOut(3000);
// });





// =================================================  CALLING API  ================================================

async function makeAPIcall() {
  await axios.get("/api/get_red_wines")
  await axios.get("/api/get_white_wines")
  await axios.get("/api/get_rose_wines")

}
async function getReds() {
  await axios.get("/api/get_red_wines")


}

async function getWhites() {
  await axios.get("/api/get_white_wines")

}

async function getRose() {
  await axios.get("/api/get_rose_wines")

}





  
    

