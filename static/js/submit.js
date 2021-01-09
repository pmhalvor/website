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

function insert(data){
    if (data.length<1){
        console.log("Empty recommendations! Try searching for and selecting a track.");
    }
    else{
        data.forEach(function(item){
            $.ajax({
                url: "submit",
                data: {'data':item},
                success: function(data){
                    console.log(data);
                }
            })
        })
    }
}