const wineResults = [{ Area: "Porto", Country: "Portugal", ID: 2163, Vintage: 2020 }, { Area: "Oporto", Country: "Portugal", ID: 1670, Vintage: 1983}, { Area: "Oporto", Country: "Portugal", ID: 2515, Vintage: 2002 }, { Area: "Eger", Country: "Hungary", ID: 1893, Vintage: 1990}, { Area: "Setbula Peninsula", Country: "Portugal", ID: 2371, Vintage: 1995}, { Area: "Oporto", Country: "Portugal", ID: 2030, Vintage: 2005 }, { Area: "Oporto", Country: "Portugal", ID: 2410, Vintage: 2011}]
const filters = ['Vintage (Oldest)', 'Winery (Alphabetically)', 'Vintage (Youngest)']
// sort by first Name

const index = filters.indexOf("Vintage (Youngest)")
filters.splice(index, 1)

console.log(filters);

// function sortWine() {


// var myArrayObjects = [{
//     "id": 1,
//     "name": "1 example"
//   },
//   {
//     "id": 5,
//     "name": "nv"
//   },
//   {
//     "id": 2,
//     "name": "100 example"
//   },
//   {
//     "id": 3,
//     "name": "nv"
//   },
//   {
//     "id": 4,
//     // "name": "5 example"
//   },

// ]

// myArrayObjects = myArrayObjects.sort(function(a, b) {
//   return a.name.localeCompare(b.name, undefined, {
//     numeric: true,
//     sensitivity: 'base'
//   });
// });

// console.log(myArrayObjects);
// }

// sortWine()