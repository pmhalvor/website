$("#recommend").click(function(){
    $(".recommended").each(insert(item));
    $("#recommendations").empty();
});

function insert(item){
    console.log(item);
    console.log("push to db");
    // return {'artists':item.artists, 'id':item.id, 'track':item.track};
}


// function insert_all(items){
//     if (items.length<1){
//         console.log("Empty recommendations! Try searching for and selecting a track.");
//     }
//     else{
//         console.log(items);
//         console.log(csrftoken);
//         const request = new Request(
//             "submit",
//             {headers: {'X-CSRFToken': csrftoken},
//             method: 'POST',
//             body: '{"items":'+items+'}'}
//         );
//         fetch(request).then(function(response) {
//             console.log(response.status==200);
//             console.debug(response);
//         });
        
//     }
//     console.log("finito");
// }