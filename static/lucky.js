/** processForm: get data from form and make AJAX call to our API. */
$("#lucky-form").on("submit", async function processForm(evt) {

  evt.preventDefault();

  const name = $("#name").val();
  const yearString = $("#year").val();
  const email = $("#email").val();
  const color = $("#color").val();
  const year = parseInt(yearString)
 

  const obj = await makeRequest(name, year, email, color);
 

  if (obj.errors) {
    populateErrors(obj)
  } else {
    succesfulResponse(obj)
  }
  
});
   

function populateErrors(obj) {
    if (obj.errors.name) $("#name-err").text(obj.errors.name[0])
    if (obj.errors.year) $("#year-err").text(obj.errors.year[0])
    if (obj.errors.email) $("#email-err").text(obj.errors.email[0])
    if (obj.errors.color) $("#color-err").text(obj.errors.color[0])
}

function succesfulResponse(obj) {
    response = `Your lucky number is ${obj.num.num} (${obj.num.fact}).
    Your birth year (${obj.year.year}) fact is ${obj.year.fact}.`

    $("#lucky-results").text(response)
}

async function makeRequest(name, year, email, color) {
  const res = await axios.post("/api/get-lucky-num", { name: name, year: year, email: email, color: color });
   
  obj = res.data;

  return obj

}

