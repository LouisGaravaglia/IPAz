

// This function is here so that the varietal selects do not get added upon each other when user hits the back GamepadButton.
window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted || 
                         ( typeof window.performance != "undefined" && 
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    window.location.reload();
  }
});

// =================================================  WINE TYPE  ================================================

$("#wine-type-dropdown").on("click", ".wine-type", async function(e) {
  const selected_button = e.target;
  selected_button.classList.add("is-active")
  wine_type = selected_button.innerText

  if (wine_type == 'Red') {
    white = e.target.nextElementSibling;
    rose = white.nextElementSibling;
    allAbove = rose.nextElementSibling;

    white.classList.remove("is-active")
    rose.classList.remove("is-active")
    allAbove.classList.remove("is-active")
  } else if (wine_type == "White") {
    red = e.target.previousElementSibling;
    rose = e.target.nextElementSibling;
    allAbove = rose.nextElementSibling;

    red.classList.remove("is-active")
    rose.classList.remove("is-active")
    allAbove.classList.remove("is-active")

  } else if (wine_type == "Rose") {
    white = e.target.previousElementSibling;
    red = white.previousElementSibling;
    allAbove = e.target.nextElementSibling;

    white.classList.remove("is-active")
    red.classList.remove("is-active")
    allAbove.classList.remove("is-active")

  } else {
    red = white.previousElementSibling;
    rose = e.target.previousElementSibling;
    white = rose.previousElementSibling;

    red.classList.remove("is-active")
    rose.classList.remove("is-active")
    white.classList.remove("is-active")
  }


  await sendWineType(wine_type)
  
})

async function sendWineType(wine_type) {
  const res = await axios.get(`/wine_type/${wine_type}`)
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


$("#varietals").on("click", ".varietals", async function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
  varietal = selected_button.innerText
  console.log("clickng");
  await sendVarietals(varietal)
})



async function sendVarietals(varietal) {
  const res = await axios.get(`/show_combined_question/${varietal}`)
}

async function makeAPIcall() {
  await axios.get("/api/get_red_wines")
  await axios.get("/api/get_white_wines")
  await axios.get("/api/get_rose_wines")

}




  
    

