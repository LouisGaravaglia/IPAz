

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
  console.log(selected_button.innerText);



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
 
  populateWineResults(wine_results.data.wine_results)
  
})

function populateWineResults(wine_results) {
  wineHtml = $("#wine-results")
  wineHtml.html("")


for (wine of wine_results) {

  
  const html = `<div class="column is-half">
  <div class="has-text-centered">
  </div>

  <div class="card">
  <header class="card-header">
    <p class="card-header-title">
      Wine
    </p>
    <a href="#" class="card-header-icon" aria-label="more options">
      <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
    </a>
  </header>
  <div class="card-content">
    <div class="content">
    <p>NAME: ${wine['Name']}</p>
    <p>WINERY: ${wine['Winery']}</p>
    <p>COUNTRY: ${wine['Country']}</p>
    <p>AREA: ${wine['Area']}</p>
    <p>VINTAGE: ${wine['Vintage']}</p>
    <p>VARIETAL: ${wine['Varietal']}</p>
    <p>TYPE: ${wine['Type']}</p>
    <p>RATING: ${wine['Rating']}</p>
      
    </div>
  </div>
  <footer class="card-footer">
    <a href="#" class="card-footer-item">Favorite</a>
    <a href="#" class="card-footer-item">Review</a>
  </footer>
</div>
</div>`

wineHtml.append(html)

}
}



// =================================================  FILTER BY / HOME PAGE ================================================

$("#filter-by").on("click", ".filter-by", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  filterBy = selected_button.innerText
  console.log(e.target);


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

async function toggleFilters(sibling, siblingName, targetInput, filterName ) {
          await sendSortBy(filterName)
          const wine_results = await axios.get(`/wine_style/""`)
          populateWineResults(wine_results.data.wine_results)

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

$("#checkboxes").on("click", ".panel-block", async function(e) {
  const target = e.target;
  // console.log(target.parentElement.firstElementChild);
  
  // console.log(target.parentElement.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild);
  // if (target.tagName == "LABEL") {
    
  // } else 

  if (target.tagName == "INPUT") {
    const filterName = target.nextSibling.data;
    const targetInput = target.parentElement.firstElementChild;

      if (filterName == 'Red') {
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
        populateWineResults(wine_results.data.wine_results)

      } else if (filterName == 'White') {
          allAbove = target.parentElement.parentElement.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild;
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
        populateWineResults(wine_results.data.wine_results)

      } else if (filterName == 'Rose') {
          allAbove = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
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
        populateWineResults(wine_results.data.wine_results)

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
        populateWineResults(wine_results.data.wine_results)

    } else if (filterName == 'Rating (Highest)') {
          ratingLowest = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Rating (Lowest)'
          toggleFilters(ratingLowest, siblingName, targetInput, filterName ) 

    } else if (filterName == 'Rating (Lowest)') {
          ratingHighest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Rating (Highest)'
          toggleFilters(ratingHighest, siblingName, targetInput, filterName )

    } else if (filterName == 'Vintage (Oldest)') {
          vintageYoungest = target.parentElement.parentElement.nextElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Vintage (Youngest)'
          toggleFilters(vintageYoungest, siblingName, targetInput, filterName )

    } else if (filterName == 'Vintage (Youngest)') {
          vintageOldest = target.parentElement.parentElement.previousElementSibling.firstElementChild.firstElementChild;
          siblingName = 'Vintage (Oldest)'
          toggleFilters(vintageOldest, siblingName, targetInput, filterName )

    } else if (filterName == 'Winery (Alphabetically)') {
          await sendSortBy(filterName)
          const wine_results = await axios.get(`/wine_style/""`)
          populateWineResults(wine_results.data.wine_results)

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
 
  populateWineResults(wine_results.data.wine_results)

})


// =================================================  CALLING API  ================================================

async function makeAPIcall() {
  await axios.get("/api/get_red_wines")
  await axios.get("/api/get_white_wines")
  await axios.get("/api/get_rose_wines")

}




  
    

