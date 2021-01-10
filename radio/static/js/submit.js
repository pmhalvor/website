$("#recommend").click(function(){
    $(".recommended").each(insert);
    $("#recommendations").empty();
});

function insert(){
    console.log("inserting row...");
    var artists = get_artists($(this));
    var track = $(this).find("#track").html();
    var track_id = this.id;
    var data = {
        'artists': artists,
        'track': track,
        'track_id': track_id,
    }
    console.log(artists, track, track_id);

    console.log("getting token...");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    console.log("pushing to db...");
    $.ajax({
        url:"submit",
        data: data,
        'X-CSRFToken': csrftoken,
        success:function(response){
            console.log(response);
            console.log("insert complete");
        }
    });
}

function get_artists(entry){
    var a = [];
    entry.find(".person").each(function(){
        a.push($(this).html());
    });
    return a;
}
