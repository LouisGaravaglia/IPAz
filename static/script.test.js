// const { TestResult } = require("@jest/types");

// const paginate = require('./paginate');

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

describe("populate wine results", function () {

  it("should populate the correct wine card depending on the values", function () {
    const wineResults = [{'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}, {'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}, {'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}, {'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}, {'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}, {'ID':4, 'Rating':87, 'Winery':"test winery1", 'Country':"test country 2", 'Vintage':"2007", 'Area':"test area 1", 'Varietal':"Barbera", 'Type':"Red", 'Name':"Test Wine 1"}]
    const wineArray1 = paginate(1, wineResults);
    const wineArray2 = paginate(2, wineResults);
    const wineArray4 = paginate(4, wineResults);
    const wineArray6 = paginate(6, wineResults);
    const wineArray8 = paginate(8, wineResults);
    expect(wineArray1.length).toEqual(6);
    expect(wineArray2.length).toEqual(3);
    expect(wineArray4.length).toEqual(2);
    expect(wineArray6.length).toEqual(1);
    expect(wineArray8.length).toEqual(1);
  });

});






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


// describe('The menu', function() {
//     // Add a spyOnEvent
//     let spyEvent;

//     beforeEach(function() {
//         // I assumed your menu icon has a unique ID of 'menuIconID'
//         // so I passed onto a spy listener.
//         spyEvent = spyOnEvent('#main-pagination', 'click');
//     });
//     it('the menu changes visibility when the menu icon is clicked', function() {

//         // Click once
//         $("#main-pagination").trigger("click");
//         expect('click').toHaveBeenTriggeredOn('#main-pagination');
//         expect(spyEvent).toHaveBeenTriggered();
//         // menu = $('body').attr('class'); // assign the new class
//         // expect(menu).toBe('');

//         // Click again
//         $("#main-pagination").trigger("click");
//         expect('click').toHaveBeenTriggeredOn('#main-pagination');
//         expect(spyEvent).toHaveBeenTriggered();
//         // menu = $('body').attr('class'); // update the new class
//         // expect(menu).toBe('menu-hidden');
//     });
// });


// $("#main-pagination").on("click", ".main-pagination-next", function() {
//   const currentPage = sessionStorage.getItem("currentPage");
//   const nextPage = parseInt(currentPage) + 1;
//   sessionStorage.setItem("currentPage", nextPage)
//   if (nextPage > 0 && $(".main-pagination-previous").hasClass("hidden")) {
//     $(".main-pagination-previous").removeClass("hidden")
//   }
//   if (currentPage == paginatedWine.length - 2 && !$(".main-pagination-next").hasClass("hidden")) {
//     $(".main-pagination-next").addClass("hidden")
//   }
//   populateWineResults(paginatedWine[nextPage], favs, reviews) 
// })

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
