

// This function is here so that the varietal selects do not get added upon each other when user hits the back GamepadButton.
// window.addEventListener( "pageshow", function ( event ) {
//   var historyTraversal = event.persisted || 
//                          ( typeof window.performance != "undefined" && 
//                               window.performance.navigation.type === 2 );
//   if ( historyTraversal ) {
//     window.location.reload();
//   }
// });

// =================================================  WINE TYPE / HOME PAGE  ================================================

$("#wine-type").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  wine_type = selected_button.innerText
  varietalDiv = $("#varietals")
  varietalDiv.html("")

    if (wine_type == 'Red') {
      allAbove = e.target.nextElementSibling.nextElementSibling.nextElementSibling;
      if (allAbove.classList.contains("is-focused")) {
          allAbove.classList.remove("is-focused")
          await sendWineType('All of the above')
      }
    } else if (wine_type == 'White') {
        allAbove = e.target.nextElementSibling.nextElementSibling;
        if (allAbove.classList.contains("is-focused")) {
           allAbove.classList.remove("is-focused")
           await sendWineType('All of the above')
        }
    } else if (wine_type == 'Rose') {
        allAbove = e.target.nextElementSibling;
        if (allAbove.classList.contains("is-focused")) {
           allAbove.classList.remove("is-focused")
           await sendWineType('All of the above')
        }
    } else {
        rose = e.target.previousElementSibling;
        white = rose.previousElementSibling;
        red = white.previousElementSibling;

        if (rose.classList.contains("is-focused")) {
           rose.classList.remove("is-focused")
           await sendWineType('Rose')
        }

        if (white.classList.contains("is-focused")) {
           white.classList.remove("is-focused")
           await sendWineType('White')
        }

        if (red.classList.contains("is-focused")) {
           red.classList.remove("is-focused")
           await sendWineType('Red')
        }
    }

  await sendWineType(wine_type)

  const items = await axios.get('/get_varietals')
  varietal_array = items.data.varietals;
  selected_varietals = items.data.selected_varietals;

  populateVarietals(varietal_array, selected_varietals)
  
})

async function sendWineType(wine_type) {
  const res = await axios.get(`/wine_type/${wine_type}`)
}

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

// =================================================  WINE STYLE / RESULTS PAGE  ================================================

$("#wine-style").on("click", ".wine-style", async function(e) {
  const selected_button = e.target.parentElement;
   




  if (selected_button.classList.contains("is-active")) {
    return
  } else {
    if (selected_button.innerText == 'All') {
      const blends = selected_button.nextElementSibling;
      const single = blends.nextElementSibling;

      blends.classList.remove("is-active");
      single.classList.remove("is-active");
    } else if (selected_button.innerText == 'Blends Only') {
      const all = selected_button.previousElementSibling;
      const single = selected_button.nextElementSibling;

      all.classList.remove("is-active");
      single.classList.remove("is-active");
    } else {
      const blends = selected_button.previousElementSibling;
      const all = blends.previousElementSibling;

      blends.classList.remove("is-active");
      all.classList.remove("is-active");
    }
  }

  selected_button.classList.toggle("is-active")

  wineStyle = selected_button.innerText

  const wine_results = await axios.get(`/wine_style/${wineStyle}`)
  wines = wine_results.data.wine_results;
  favs = wine_results.data.user_favorites;
 
  populateWineResults(wines, favs)
  
})

const userFavorite = function(wine) {

  const html = `<div class="column is-half">
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
      <button class="button is-dark favorite-button" data-id="${wine['ID']}">
        <span class="icon is-small">
        <i class="fas fa-thumbtack"></i>
        </span>
      </button>
    </div>
    <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
    <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
      <button class="button is-text review-btn" data-id="${wine['ID']}>
        <span class="icon is-small is-right review-btn">
        <i class="fas fa-pen review-btn"></i>
        </span>
      </button>
      </form>
    </div>
  </div>
</article>

  </div>`

  return html;

}

const notFavorite = function(wine){

const html = `<div class="column is-half">
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
        <span class="icon is-small">
        <i class="fas fa-thumbtack"></i>
        </span>
      </button>
    </div>
    <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
    <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
      <button class="button is-text review-btn" data-id="${wine['ID']}>
        <span class="icon is-small is-right review-btn">
        <i class="fas fa-pen review-btn"></i>
        </span>
      </button>
      </form>
    </div>
  </div>
</article>

  </div>`

  return html;

}

function populateWineResults(wine_results, favorites) {
  wineHtml = $("#wine-results")
  wineHtml.html("")
  
  if (wine_results[0] == "No Results") {
    
    const html = '<h3 class="title is-3 has-text-centered mt-6">No wines available.</h3>'
    wineHtml.append(html)

  } else {

    for (wine of wine_results) {

      if (favorites.includes(wine['ID'])) {
  
        const html = userFavorite(wine)
        wineHtml.append(html)

      } else {

        const html = notFavorite(wine)
        wineHtml.append(html)

      }
    }
  }
}

// =================================================  FAVORITE BUTTON ================================================


const getFavList = async function(wineId) {
  const fav_wine_list = await axios.post(`/user/add_favorite/${wineId}`)
  const wine_results = await axios.get(`/wine_style/""`)
  wines = wine_results.data.wine_results;
  favs = fav_wine_list.data.fav_wine_list;
  populateWineResults(wines, favs)
}

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

// =================================================  VIEWING FAVORITES ================================================

function populateFavorites(favorites) {
  favoritesHtml = $("#wine-favorites")
  favoritesHtml.html("")
  
  if (favorites[0] == "No Results") {

    const html = '<h3 class="title is-3 has-text-centered mt-6">No favorites yet.</h3>'
    favoritesHtml.append(html)

  } else {

    for (wine of favorites) {

    
  const html = `<div class="column is-one-third">
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
      <button class="button is-dark fav-button favorite-button" data-id="${wine['ID']}" type="submit">
        <span class="icon is-small">
        <i class="fas fa-thumbtack"></i>
        </span>
      </button>
      
    </div>
    <div class="column is-half has-text-centered mx-0 my-0" id="review-btn">
      <form method="POST" action="/user/review/${wine['ID']}" id="review-form">
      <button class="button is-text review-btn" data-id="${wine['ID']}">
        <span class="icon is-small is-right review-btn">
        <i class="fas fa-pen review-btn"></i>
        </span>
      </button>
      </form>
    </div>
  </div>

</article>
</div>`
   favoritesHtml.append(html)
      } 
  }
}


const getFavs = async function(wineId) {
  const favs = await axios.post(`/user/add_favorite/${wineId}`)
  favorites = favs.data.fav_wines;
  populateFavorites(favorites)

}

  $("#wine-favorites").on("click", ".favorite-button", async function(e) {
    const target = e.target;

    if (target.tagName == "BUTTON") {
      let wineId = target.dataset.id;
      getFavs(wineId);
     

    } else if (target.tagName == "path") {
      const button = target.parentElement.parentElement.parentElement;
      let wineId = button.dataset.id;
      getFavs(wineId);

    } else if (target.tagName == "SPAN") {
      const button = target.parentElement;
      let wineId = button.dataset.id;
      getFavs(wineId);

    } else if (target.tagName == "svg") {
      const button = target.parentElement.parentElement;
      let wineId = button.dataset.id;
      getFavs(wineId);
    }
  })

// =================================================  REVIEW BUTTON ================================================



// $("#review-btn").on("click", ".review-btn", async function(e) {
//   console.log(e);
//   // const res = await axios.post("/user/add_like/<int:wine_id>")

//   // const wine_results = await axios.get(`/wine_style/""`)
//   // wines = wine_results.data.wine_results;
//   // favs = wine_results.data.user_favorites;
 
//   // populateWineResults(wines, favs)

// })


// =================================================  FILTER BY / HOME PAGE ================================================

$("#filter-by").on("click", ".filter-by", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  filterBy = selected_button.innerText
  


  if (filterBy == 'Rating (Highest)') {
      ratingLowest = e.target.nextElementSibling;
      if (ratingLowest.classList.contains("is-focused")) {
          ratingLowest.classList.remove("is-focused")
          await sendSortBy('Rating (Lowest)')
      }
    } else if (filterBy == 'Rating (Lowest)') {
        ratingHighest = e.target.previousElementSibling;
        if (ratingHighest.classList.contains("is-focused")) {
           ratingHighest.classList.remove("is-focused")
           await sendWineType('Rating (Highest)')
        }
    } else if (filterBy == 'Vintage (Oldest)') {
        vintageYoungest = e.target.nextElementSibling;
        if (vintageYoungest.classList.contains("is-focused")) {
           vintageYoungest.classList.remove("is-focused")
           await sendWineType('Vintage (Youngest)')
        }
    } else if (filterBy == 'Vintage (Youngest)') {
        vintageOldest = e.target.previousElementSibling;
        if (vintageOldest.classList.contains("is-focused")) {
           vintageOldest.classList.remove("is-focused")
           await sendWineType('Vintage (Oldest)')
        }
    } 



  await sendSortBy(filterBy)
  
})

async function sendSortBy(filterBy) {
  const res = await axios.get(`/sort_by/${filterBy}`)
}

// =================================================  LOADING VARIETALS / HOME PAGE ================================================

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

// =================================================  PICKING FILTERS / RESULTS PAGE  ================================================

async function toggleSortByFilter(sibling, siblingName, targetInput, filterName ) {
          await sendSortBy(filterName)
          const wine_results = await axios.get(`/wine_style/""`)
          wines = wine_results.data.wine_results;
          favs = wine_results.data.user_favorites;
          populateWineResults(wines, favs)

          if (sibling.classList.contains("is-focused")) {
            sibling.classList.remove("is-focused");
            await sendSortBy(siblingName)
          } 
          if (targetInput.classList.contains("is-focused")) {
          targetInput.classList.remove("is-focused")
        } else {
          targetInput.classList.add("is-focused")
        }   
}

async function toggleWineTypeFilter(target, filterName, targetInput) {
        allAbove = target.parentElement.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild;
        const res = await axios.get(`/wine_type/${filterName}`)
        
        if (allAbove.classList.contains("is-focused")) {
          allAbove.classList.remove("is-focused");
          const res = await axios.get(`/wine_type/'All of the above'`)
         
        }
        if (targetInput.classList.contains("is-focused")) {
          targetInput.classList.remove("is-focused")
        } else {
          targetInput.classList.add("is-focused")
        }

        const wine_results = await axios.get(`/wine_style/""`)
        wines = wine_results.data.wine_results;
        favs = wine_results.data.user_favorites;
        populateWineResults(wines, favs)
}

$("#checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;

  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;

      if (filterName == 'Red') {
        toggleWineTypeFilter(target, filterName, targetInput)

      } else if (filterName == 'White') {
          toggleWineTypeFilter(target, filterName, targetInput)

      } else if (filterName == 'Rose') {
          toggleWineTypeFilter(target, filterName, targetInput)

    } else if (filterName == 'All of the above') {
          rose = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
          white = target.parentElement.parentElement.previousElementSibling.previousElementSibling.firstElementChild.firstElementChild;
          red = target.parentElement.parentElement.previousElementSibling.previousElementSibling.previousElementSibling.firstElementChild.firstElementChild;
          const res = await axios.get(`/wine_type/${filterName}`)
          
          if (red.classList.contains("is-focused")) {
            red.classList.remove("is-focused");
            const res = await axios.get(`/wine_type/'Red'`)
          }
          if (white.classList.contains("is-focused")) {
            white.classList.remove("is-focused");
            const res = await axios.get(`/wine_type/'White'`)
          }
          if (rose.classList.contains("is-focused")) {
            rose.classList.remove("is-focused");
            const res = await axios.get(`/wine_type/'Rose'`)
          }
          if (targetInput.classList.contains("is-focused")) {
          targetInput.classList.remove("is-focused")
        } else {
          targetInput.classList.add("is-focused")
        }

        const wine_results = await axios.get(`/wine_style/""`)
        wines = wine_results.data.wine_results;
        favs = wine_results.data.user_favorites;
        populateWineResults(wines, favs)

    } else if (filterName == 'Rating (Highest)') {
          ratingLowest = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Rating (Lowest)'
          toggleSortByFilter(ratingLowest, siblingName, targetInput, filterName ) 

    } else if (filterName == 'Rating (Lowest)') {
          ratingHighest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Rating (Highest)'
          toggleSortByFilter(ratingHighest, siblingName, targetInput, filterName )

    } else if (filterName == 'Vintage (Oldest)') {
          vintageYoungest = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Vintage (Youngest)'
          toggleSortByFilter(vintageYoungest, siblingName, targetInput, filterName )

    } else if (filterName == 'Vintage (Youngest)') {
          vintageOldest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Vintage (Oldest)'
          toggleSortByFilter(vintageOldest, siblingName, targetInput, filterName )

    } else if (filterName == 'Winery (Alphabetically)') {
          await sendSortBy(filterName)
          const wine_results = await axios.get(`/wine_style/""`)
          wines = wine_results.data.wine_results;
          favs = wine_results.data.user_favorites;
          populateWineResults(wines, favs)

          if (targetInput.classList.contains("is-focused")) {
          targetInput.classList.remove("is-focused")
        } else {
          targetInput.classList.add("is-focused")
        }
           
         
    }  
  }

})


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
  populateWineResults(wines, favs)

})


// =================================================  CALLING API  ================================================

async function makeAPIcall() {
  await axios.get("/api/get_red_wines")
  await axios.get("/api/get_white_wines")
  await axios.get("/api/get_rose_wines")

}




  
    

