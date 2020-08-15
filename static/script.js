$("#make-call").on("submit", async function processForm(evt) {

  evt.preventDefault();


  const obj = await makeRequest();

  data = obj.items[0];

  console.log(data);

});
   

async function makeRequest() {
  // const BASE_URL = "http://localhost:5000/"

  const res = await axios.get("/api/get_top_rated");
   
  obj = res.data;

  return obj

}
