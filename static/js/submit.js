$("#recommend").click(function(){
    var submitted = [];
    $(".recommended").each( function() {
        var artists = [];
        $(this).find(".person").each(function(){
            artists.push($(this).text());
        });
        var track  = $(this).find("#track").text();
        var id = this.id;
        submitted.push({'artists':artists, 'track':track, 'id':id});
    });
    $("#recommendations").empty();
    console.log(submitted);
});