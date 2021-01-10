$("#recommend").click(function(){
    $(".recommended").each(insert);
    $("#recommendations").empty();
});

function insert(){
    var artists = get_artists($(this));
    var track = $(this).find("#track").html();
    var track_id = this.id;
    var data = {
        'artists': artists,
        'track': track,
        'track_id': track_id,
    }
    console.log(data);

    console.log("getting token...");
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken);
    
    console.log("pushing to db...");
    $.ajax({
        url:"submit",
        data: data,
        'X-CSRFToken': csrftoken,
        success:function(response){
            console.debug(response);
        }
    });

    console.log("complete.");
}

function get_artists(entry){
    var a = [];
    entry.find(".person").each(function(){
        a.push($(this).html());
    });
    return a;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}