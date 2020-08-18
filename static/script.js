

// This function is here so that the varietal selects do not get added upon each other when user hits the back GamepadButton.
window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted || 
                         ( typeof window.performance != "undefined" && 
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    window.location.reload();
  }
});



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




  
    

