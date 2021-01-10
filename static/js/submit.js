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
        // data.forEach( function(item){
        //     console.log(item);
        //     // $.ajax({
        //     //     url: "submit",
        //     //     data: JSON.stringify(item),
        //     //     dataType:"json",
        //     //     type: "POST",
        //     //     success: function(data, textStatus, xhr){
        //     //         console.log(data);
        //     //         console.log(textStatus);
        //     //         console.log(xhr);
        //     //     }
        //     // });
        //     $.post("submit", item, function(response){
        //         alert(response);
        //     });
        // });
        $.ajax({
            url:"submit",
            data: {'items':items},
            success: function(response){
                console.log(response);
            }
        });
    }
    console.log("finito");
}