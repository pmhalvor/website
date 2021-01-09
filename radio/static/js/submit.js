$("#recommend").click(function(){
    var submitted = [];
    $(".recommended").each( function() {
        var artists = [];
        $(this).find(".person").each(function(){
            artists.push($(this).text());
        });
        var track  = $(this).find("#track").text();
        var id = this.id;
        var time = $(this).find("#time").text();
        submitted.push({'artists':artists, 'id':id, 'sub_time':time, 'track':track});
    });
    $("#recommendations").empty();
    console.log(submitted);
});