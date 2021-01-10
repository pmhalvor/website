$("#recommend").click(function(){
    var submitted = [];
    $(".recommended").each( function() {
        var artists = [];
        $(this).find(".person").each(function(){
            artists.push($(this).text());
        });
        var track  = $(this).find("#track").text();
        var id = this.id;
        submitted.push({'artists':artists, 'id':id, 'track':track});
    });
    $("#recommendations").empty();
    insert(submitted);
});

function insert(items){
    if (items.length<1){
        console.log("Empty recommendations! Try searching for and selecting a track.");
    }
    else{
        console.log(csrftoken);
        console.log(items);
        const request = new Request(
            "submit",
            {headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            body: '{"items":'+items+'}'}
        );
        fetch(request).then(function(response) {
            console.log(response.status==200);
            console.debug(response);
        });
        
    }
    console.log("finito");
}