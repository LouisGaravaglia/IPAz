const wineResults = [{"key":"one"},{"key":"two"},{"key":"three"},{"key":"four"},{"key":"five"},{"key":"six"},{"key":"seven"},{"key":"eight"},{"key":"nine"},{"key":"ten"},{"key":"eleven"},{"key":"twelve"},{"key":"thirteen"},{"last":"one"}]
// const paginated_wine = []
// const wine_group = []
// // console.log(wine_results);

// const wine_length = wine_results.length

// for (let i = 0; i < wine_length; i++) {
    
//     wine_group.push(wine_results[i]);

//     // console.log(wine_group);

//     if (i == 9) {
//         console.log(wine_group);
//         paginated_wine.push(wine_group);
//         wine_group.splice(0, wine_group.length);
        
//     }
// }

// // test_array = [1, 2, 3, 4, 5, 6]
// // console.log(test_array);
// // test_array.splice(0, test_array.length);
// // console.log(test_array);

// // for (wine in wine_results) {
// //         const wine_group = []
      
// //         wine_length = wine_results.length
// //         wine_group.push(wine);
    
// //         if (i % 10 == 0 || i == wine_length) {
// //           paginated_wine.push(wine_group);
// //           wine_group.splice(0, wine_group.length);
          
// //         }
// //         i++
// //       }

// // console.log(wine_group);
// console.log(paginated_wine);

let a, b
let paginatedWine = []

for (a = 0; a <= wineResults.length; a += 10) {
    let wineGroup = [];
    for (b = 0; b <= 9; b++) {
        wineGroup.push(wineResults[b+a])
        if ( a+b >= wineResults.length - 1) {
            paginatedWine.push(wineGroup)
            console.log(paginatedWine);
            return
        }
    }
    paginatedWine.push(wineGroup)
}

// console.log(paginatedWine);