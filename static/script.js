// $("#make-call").on("submit", async function processForm(evt) {

//   evt.preventDefault();


//   const obj = await makeRequest();

//   data = obj.items[0];

//   console.log(data);

// });
   

// async function makeRequest() {
//   // const BASE_URL = "http://localhost:5000/"

//   const res = await axios.get("/api/get_top_rated");
   
//   obj = res.data;

//   return obj

// }

$("#varietals").on("click", ".varietals", function(e) {
  const selected_button = e.target;
  selected_button.classList.toggle("is-focused")
})

$("#varietals-submit").on("click", function(e) {
$("#hidden-selects").val([])
var varietals = $('.vareitals');
const varietal_selects = [];
$(".varietals").each(function(index, value) {
  
  if ($(value).hasClass('is-focused')) {
    varietal_selects.push(value.innerText)
  }
})

$("#hidden-selects").val(varietal_selects)
sendVarietals()
})

const sendVarietals = async function() {
  const varietal_selects = $("#hidden-selects").val();
  await axios.get(`/show_combined_question/${varietal_selects}`)
  window.location.href = 'http://127.0.0.1:5000/show_combined_question';
}

$("#combined-question").on("click", function(e) {
  
  // console.log($("#hidden-selects").val());
  // const varietal_selects = $("#hidden-selects").val();
  // const one = varietal_selects[0]
  // axios.post("http://127.0.0.1:5000/show_wine_results", {selections: one});
})


  
    


// $("#combined-varietals").on("click", ".combined-varietals", function(e) {
//   const selected_button = e.target;
//   selected_button.classList.toggle("is-focused")
// })
