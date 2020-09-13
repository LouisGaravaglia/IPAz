// describe("populate wine results", function () {

//   it("should populate the correct wine card depending on the values", function () {
//         const wineDiv = document.createElement('div');
//         wineDiv.id = "wine-results"
//         wineDiv.innerHTML = "HII"
//         wineDiv.setAttribute( 'class', 'columns my-3 mx-3 is-multiline' )
//         populateWineResults(['No Results'])
//     expect(
//       wineDiv.innerHTML
//       ).toEqual('<div class="columns my-3 mx-3 is-multiline" id="wine-results"><section class="hero is-small is-light mt-6 mx-6"><div class="hero-body"><div class="container"><h1 class="title has-text-info">No wines available.</h1></div></div></section></div>')
//   });



// });



//  */
// function toggleStar(icon, wineId){
//   if (icon.hasClass("myFas")) {
//     icon.removeClass("myFas")
//     icon.addClass("myFar")
//     icon.html(`<i class="far fa-star" data-id="${wineId}"></i>`)
//   } else {
//     icon.removeClass("myFar")
//     icon.addClass("myFas")
//     icon.html(`<i class="fas fa-star" data-id="${wineId}"></i>`)
//   }
// }

// describe("toggle favorite star", function () {

//   it("should toggle the favorite star from filled to outline", function () {
//         const iconBtn = document.createElement('button');
//         iconBtn.id = "my-button"
//         iconBtn.setAttribute( 'class', 'myFas' )
//         const wineId = "2334"
//         const icon = $("#my-button")
//         toggleStar(icon, wineId)
//     expect(
//       iconBtn.classList
//       ).toContain('myFar')
//       expect(
//       iconBtn.html
//       ).toEqual(`<i class="fas fa-star" data-id="${wineId}"></i>`)
//   });

// });


// describe("populate wine results", function () {
//   var wineHtml;

//   beforeEach(function(){
//     wineHtml = $("#wine-results");
//     wineHtml.innerHTML = '<div class="columns my-3 mx-3 is-multiline" id="wine-results"></div>'
//     $(document.body).append(wineHtml);
//     populateWineResults(["No Results"])
//   });


//   it("should populate the correct wine card depending on the values", function () {
//     expect(
//       wineHtml.innerHTML
//       ).toEqual('<div class="columns my-3 mx-3 is-multiline" id="wine-results"><section class="hero is-small is-light mt-6 mx-6"><div class="hero-body"><div class="container"><h1 class="title has-text-info">No wines available.</h1></div></div></section></div>')
//   });


//   afterEach(function(){
//    wineHtml.remove();
//    wineHtml = null;
//   });

// });
