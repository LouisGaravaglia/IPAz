

// This function is here so that the user favorites get updated in the show_results route if the user
// hits back from the favorties route after unfavoriting a wine.
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

$("#wine-type").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  wine_type = selected_button.innerText
  varietalDiv = $("#varietals")
  varietalDiv.html("")

  await sendWineType(wine_type)

  const items = await axios.get('/get_varietals')
  varietal_array = items.data.varietals;
  selected_varietals = items.data.selected_varietals;

  populateVarietals(varietal_array, selected_varietals)
  
})

async function sendWineType(wine_type) {
  const res = await axios.get(`/wine_type/${wine_type}`)
}

// =================================================  SORT BY / HOME PAGE ================================================

$("#filter-by").on("click", ".filter-by", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  filterBy = selected_button.innerText
  
  await sendSortBy(filterBy)
  
})

async function sendSortBy(filterBy) {
  const res = await axios.get(`/sort_by/${filterBy}`)
}

// =================================================  LOADING VARIETALS / HOME PAGE ================================================
function populateVarietals(varietal_array, selected_varietals) {

for (varietal of varietal_array) {
  if (selected_varietals.includes(varietal)) {
    html = `<button class="button is-primary is-outlined is-rounded is-small mt-3 mx-2 varietals is-focused">${varietal}</button>`
    varietalDiv.append(html);
  } else {
    html = `<button class="button is-primary is-outlined is-rounded is-small mt-3 mx-2 varietals">${varietal}</button>`
    varietalDiv.append(html);
  }

}
}




// =================================================  PICKING VARIETALS / HOME PAGE  ================================================


$("#varietals").on("click", ".varietals", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  varietal = selected_button.innerText
  await sendVarietals(varietal)
})



async function sendVarietals(varietal) {
  const res = await axios.get(`/log_varietals/${varietal}`)
}






// =================================================  POPULATE WINE RESULTS ================================================

const addWineCard = function(wine, favBtn, reviewBtn, reviewHTML, cardSize) {

  const html = `<div class="column ${cardSize}">
  <div class="has-text-centered">
  </div>

<article class="message is-dark">
  
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
    <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
      <button class="button is-text review-btn" data-id="${wine['ID']}>
        <span class="icon review-btn">
        ${reviewBtn}
        </span>
      </button>
      </form>
    </div>
  </div>
  ${reviewHTML}
</article>
  </div>`

  return html;

}

// const notFavorite = function(wine){

// const html = `<div class="column is-half">
//   <div class="has-text-centered">
//   </div>

// <article class="message is-dark">
  
//   <div class="message-header">
//     <p>${wine['Name']}</p>
//   </div>

//   <div class="message-body">
//     <p><strong>NAME: </strong>${wine['Name']}</p>
//     <p><strong>WINERY: </strong>${wine['Winery']}</p>
//     <p><strong>COUNTRY: </strong>${wine['Country']}</p>
//     <p><strong>AREA: </strong>${wine['Area']}</p>
//     <p><strong>VINTAGE: </strong>${wine['Vintage']}</p>
//     <p><strong>VARIETAL: </strong>${wine['Varietal']}</p>
//     <p><strong>TYPE: </strong>${wine['Type']}</p>
//     <p><strong>RATING: </strong>${wine['Rating']}</p>
//   </div>

//   <div class="columns">
//     <div class="column is-half has-text-centered mx-0 my-0">
//       <button class="button is-text favorite-button" data-id="${wine['ID']}">
//         <span class="icon is-small">
//         <i class="fas fa-thumbtack"></i>
//         </span>
//       </button>
//     </div>
//     <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
//     <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
//       <button class="button is-text review-btn" data-id="${wine['ID']}>
//         <span class="icon is-small is-right review-btn">
//         <i class="fas fa-pen review-btn"></i>
//         </span>
//       </button>
//       </form>
//     </div>
//   </div>
// </article>

//   </div>`

//   return html;

// }

function populateWineResults(wine_results, favorites, reviews, fav_wines, wine_reviews) {
  wineHtml = $("#wine-results")
  wineHtml.html("")
  const address = document.location.href;


  if (wine_results[0] == "No Results") {
    
    const html = '<h3 class="title is-3 has-text-centered mt-6">No wines available.</h3>'
    wineHtml.append(html)

  } else if (address.includes("user/review")) {

   for (wine of wine_reviews) { 

    if (favorites.includes(wine['ID'])) {
        const favBtn = '<i class="fas fa-star"></i>';
        const reviewBtn = '<i class="far fa-times-circle deleteBtn"></i>';
        const cardSize = 'is-one-third';
        const reviewHTML = `<hr class="dropdown-divider"> 
                            <br>
                            <div class="message-body">
                                <p><strong>RATING: </strong>${wine['Post_rating']}</p>
                                <p><strong>REVIEW: </strong>${wine['Post_review']}</p>
                              </div>
                              <br>
                                <button class="button is-dark is-fullwidth is-outlined review-delete">
                                <span>Delete</span>
                                <span class="icon is-small">
                                  <i class="fas fa-times"></i>
                                </span>
                              </button>`
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      } else {
        const favBtn = '<i class="far fa-star"></i>';
        const reviewBtn = '<i class="far fa-times-circle deleteBtn"></i>';
        const cardSize = 'is-one-third';                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        const reviewHTML = `<hr class="dropdown-divider"> 
                            <br>
                            <div class="message-body">
                                <p><strong>RATING: </strong>${wine['Post_rating']}</p>
                                <p><strong>REVIEW: </strong>${wine['Post_review']}</p>
                              </div>
                              <br>
                                <button class="button is-dark is-fullwidth is-outlined review-delete">
                                <span>Delete</span>
                                <span class="icon is-small">
                                  <i class="fas fa-times"></i>
                                </span>
                              </button>`
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      }

    }

  } else if (address.includes("user/favorites")) {

    for (wine of fav_wines) { 

    if (favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
        const favBtn = '<i class="fas fa-star"></i>';
        const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
        const reviewHTML = "";
        const cardSize = 'is-one-third';
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = '<i class="fas fa-star"></i>';
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = '<i class="far fa-star"></i>';
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-one-third';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = '<i class="far fa-star"></i>';
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
        const favBtn = '<i class="fas fa-star"></i>';
        const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
        const reviewHTML = "";
        const cardSize = 'is-half';
        const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
        wineHtml.append(html)
      } else if (favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = '<i class="fas fa-star"></i>';
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && reviews.includes(wine['ID'])) {
          const favBtn = '<i class="far fa-star"></i>';
          const reviewBtn = '<i class="fas fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } else if (!favorites.includes(wine['ID']) && !reviews.includes(wine['ID'])) {
          const favBtn = '<i class="far fa-star"></i>';
          const reviewBtn = '<i class="far fa-edit review-btn"></i>';
          const reviewHTML = "";
          const cardSize = 'is-half';
          const html = addWineCard(wine, favBtn, reviewBtn, reviewHTML, cardSize)
          wineHtml.append(html)
      } 

    }

  }
}

// =================================================  FAVORITE BUTTON ON RESULTS PAGE ================================================


const getFavList = async function(wineId) {
  
  const json = await axios.post(`/user/add_favorite/${wineId}`)
  noUserObj = json.data

  // ##### CONDITIONAL TO CHECK TO SEE IF USER IS LOGGED IN IF NOT AN ERROR MESSAGE APPEARS #####
  if (Object.keys(noUserObj).length == 1) {
    
message = `<section class="hero is-small is-info">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        ${noUserObj.message}
      </h1>
    </div>
  </div>
</section>`

    flashDiv = $("#flash")
    flashDiv.html("");
    flashDiv.prepend(message)
    function hideMessage(){
      flashDiv.html("");
    }
    setTimeout(hideMessage, 2000);

  } else {
      const wine_results = await axios.get(`/wine_style/""`)
      wines = wine_results.data.wine_results;
      favs = json.data.fav_wine_list;
      reviews = wine_results.data.reviews;
      fav_wines = json.data.fav_wines;
      wine_reviews = json.data.wine_reviews;
      populateWineResults(wines, favs, reviews, fav_wines, wine_reviews)
  }
  
  
 
}



  // ##### CLEARS ALL FLASH MESSAGES AFTER 2 SECONDS #####

    $(document).ready(function(){ 
      flashDiv = $("#messageContainer");
        function hideMessage(){
          flashDiv.html("");
        }
        setTimeout(hideMessage, 2000);
    })

    


  $("#wine-results").on("click", ".favorite-button", async function(e) {

    const target = e.target;

    if (target.tagName == "BUTTON") {
      let wineId = target.dataset.id;
      getFavList(wineId);

    } else if (target.tagName == "path") {
      const button = target.parentElement.parentElement.parentElement;
      let wineId = button.dataset.id;
      getFavList(wineId);

    } else if (target.tagName == "SPAN") {
      const button = target.parentElement;
      let wineId = button.dataset.id;
      getFavList(wineId);

    } else if (target.tagName == "svg") {
      const button = target.parentElement.parentElement;
      let wineId = button.dataset.id;
      getFavList(wineId);

    }

  })

// =================================================  FAVORITE BUTTON ON FAVORITES PAGE ================================================

// function populateFavorites(favorites) {
//   favoritesHtml = $("#wine-favorites")
//   favoritesHtml.html("")
//   // console.log(favorites);
//   // console.log(favorites[0]);
//   if (!favorites[0]) {

//     const html = '<h3 class="title is-3 has-text-centered mt-6">No favorites.</h3>'
//     favoritesHtml.append(html)

//   } else {

//     for (wine of favorites) {

    
//   const html = `<div class="column is-one-third">
//   <article class="message is-dark">
  
//   <div class="message-header">
//     <p>${wine['Name']}</p>
//   </div>

//   <div class="message-body">
//     <p><strong>NAME: </strong>${wine['Name']}</p>
//     <p><strong>WINERY: </strong>${wine['Winery']}</p>
//     <p><strong>COUNTRY: </strong>${wine['Country']}</p>
//     <p><strong>AREA: </strong>${wine['Area']}</p>
//     <p><strong>VINTAGE: </strong>${wine['Vintage']}</p>
//     <p><strong>VARIETAL: </strong>${wine['Varietal']}</p>
//     <p><strong>TYPE: </strong>${wine['Type']}</p>
//     <p><strong>RATING: </strong>${wine['Rating']}</p>
//   </div>

//     <div class="columns">
//     <div class="column is-half has-text-centered mx-0 my-0">
//       <button class="button is-dark fav-button favorite-button" data-id="${wine['ID']}" type="submit">
//         <span class="icon is-small">
//         <i class="fas fa-thumbtack"></i>
//         </span>
//       </button>
      
//     </div>
//     <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
//       <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
//       <button class="button is-text review-btn" data-id="${wine['ID']}">
//         <span class="icon is-small is-right review-btn">
//         <i class="fas fa-pen review-btn"></i>
//         </span>
//       </button>
//       </form>
//     </div>
//   </div>

// </article>
// </div>`
//    favoritesHtml.append(html)
//       } 
//   }
// }


// const getFavs = async function(wineId) {
//   const favs = await axios.post(`/user/add_favorite/${wineId}`)
//   console.log(favs);
//   favorites = favs.data.fav_wines;
//   populateFavorites(favorites)

// }

  // $("#wine-favorites").on("click", ".favorite-button", async function(e) {
  //   const target = e.target;

  //   if (target.tagName == "BUTTON") {
  //     let wineId = target.dataset.id;
  //     getFavs(wineId);
     

  //   } else if (target.tagName == "path") {
  //     const button = target.parentElement.parentElement.parentElement;
  //     let wineId = button.dataset.id;
  //     getFavs(wineId);

  //   } else if (target.tagName == "SPAN") {
  //     const button = target.parentElement;
  //     let wineId = button.dataset.id;
  //     getFavs(wineId);

  //   } else if (target.tagName == "svg") {
  //     const button = target.parentElement.parentElement;
  //     let wineId = button.dataset.id;
  //     getFavs(wineId);
  //   }
  // })

// =================================================  REVIEW BUTTON ================================================



// $("#review-btn").on("click", ".review-btn", async function(e) {
//   console.log(e);
//   // const res = await axios.post("/user/add_like/<int:wine_id>")

//   // const wine_results = await axios.get(`/wine_style/""`)
//   // wines = wine_results.data.wine_results;
//   // favs = wine_results.data.user_favorites;
 
//   // populateWineResults(wines, favs)

// })



// =================================================  TOGGLE OPEN SORT BY OPTIONS / RESULTS PAGE  ================================================

$("#choose-wine-type").on("click", function(e) {
  $("#wine-type-checkboxes").toggleClass("hidden")
})

$("#choose-wine-style").on("click", function(e) {
  $("#wine-style-checkboxes").toggleClass("hidden")
})

$("#choose-sort-by").on("click", function(e) {
  $("#sort-by-checkboxes").toggleClass("hidden")
})
// =================================================  CLICK EVENT FOR WINE OPTIONS / RESULTS PAGE  ================================================

$("#wine-type-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;

  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    $(targetInput).toggleClass("is-focused")
    const res = await axios.get(`/wine_type/${filterName}`)
    const wine_results = await axios.get(`/wine_style/""`)
    wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    populateWineResults(wines, favs, reviews)

  }

})

$("#wine-style-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;

  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    $(targetInput).toggleClass("is-focused")
    const wine_results = await axios.get(`/wine_style/${filterName}`)
    wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;

    populateWineResults(wines, favs, reviews)

  }

})


$("#sort-by-checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;

  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;
    $(targetInput).toggleClass("is-focused")
    const res = await axios.get(`/sort_by/${filterName}`)
    const wine_results = await axios.get(`/wine_style/""`)
    wines = wine_results.data.wine_results;
    favs = wine_results.data.user_favorites;
    reviews = wine_results.data.reviews;
    populateWineResults(wines, favs, reviews)

  }

})

// =================================================  LOADING VARIETALS / RESULTS PAGE ================================================


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


$(".modal").on("click", ".delete", function() {
  modal = $(".modal");
  modal.toggleClass("is-active")
})

function makeModal(varietal_array, selected_varietals) {

for (varietal of varietal_array) {
  if (selected_varietals.includes(varietal)) {
    html = `<button class="button is-primary is-outlined is-rounded is-small mt-3 mx-2 varietals is-focused">${varietal}</button>`
    varietalDiv.append(html);
  } else {
    html = `<button class="button is-primary is-outlined is-rounded is-small mt-3 mx-2 varietals">${varietal}</button>`
    varietalDiv.append(html);
  }

}
}


// =================================================  PICKING VARIETALS / RESULTS PAGE  ================================================




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



$("#varietals-modal").on("click", ".varietals", async function(e) {
  const target = e.target;
  const targetName = target.innerText;

  target.classList.toggle("is-focused")
  
  await sendVarietals(targetName)
})


$("#modal").on("click", ".toggle-off", async function() {
  modal = $(".modal");
  modal.toggleClass("is-active")

  const wine_results = await axios.get(`/wine_style/""`)
  wines = wine_results.data.wine_results;
  favs = wine_results.data.user_favorites;
  reviews = wine_results.data.reviews;
  populateWineResults(wines, favs, reviews)

})


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





  
    

