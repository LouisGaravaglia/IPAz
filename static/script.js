

// This function is here so that the varietal selects do not get added upon each other when user hits the back GamepadButton.
// window.addEventListener( "pageshow", function ( event ) {
//   var historyTraversal = event.persisted || 
//                          ( typeof window.performance != "undefined" && 
//                               window.performance.navigation.type === 2 );
//   if ( historyTraversal ) {
//     window.location.reload();
//   }
// });

// =================================================  WINE TYPE  ================================================

$("#wine-type").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  wine_type = selected_button.innerText

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
  
})

async function sendWineType(wine_type) {
  const res = await axios.get(`/wine_type/${wine_type}`)
}

$("#wine-type").on("click", ".wine-type", async function() {
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

// =================================================  WINE STYLE  ================================================

$("#wine-style-dropdown").on("click", ".wine-style", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-active")
  wineStyle = selected_button.innerText


  await sendWineStyle(wineStyle)
  
})

async function sendWineStyle(wineStyle) {
  const res = await axios.get(`/wine_style/${wineStyle}`)
}

// =================================================  SORT BY  ================================================

$("#sort-by-dropdown").on("click", ".sort-by", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-active")
  sortBy = selected_button.innerText


  await sendSortBy(sortBy)
  
})

async function sendSortBy(sortBy) {
  const res = await axios.get(`/sort_by/${sortBy}`)
}

// =================================================  LOADING VARIETALS  ================================================

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


// =================================================  PICKING VARIETALS  ================================================


$("#varietals").on("click", ".varietals", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  varietal = selected_button.innerText
  await sendVarietals(varietal)
})



async function sendVarietals(varietal) {
  const res = await axios.get(`/log_varietals/${varietal}`)
}

// =================================================  SIDE BAR FILTER FOR RESULTS PAGE  ================================================

$("#checkboxes").on("click", ".panel-block", function(e) {
  const target = e.target;
  
  if (target.tagName == "LABEL") {
    
  } else if (target.tagName == "INPUT") {
    console.log(target);
    console.log(target.nextSibling.data);
  }
})

// =================================================  CALLING API  ================================================

async function makeAPIcall() {
  await axios.get("/api/get_red_wines")
  await axios.get("/api/get_white_wines")
  await axios.get("/api/get_rose_wines")

}




  
    

