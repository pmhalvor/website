// SEARCH SCRIPT
var query = null;
// from search bar to backend
$(document).ready(function(){
    $('#query').keypress(function(e){ // press enter
        if(e.keyCode==13){
            loading();
            query = $(this).val();
            searchSpotify(query);
        }
    });
    $("#search").click(function() { //press search button
        loading();
        query = $('#query').val();
        searchSpotify(query);
    });
});

function loading(){
    $("#results").html("<img src='{% static 'img/loading.gif' %}' id='loading'>");
}

function searchSpotify(q){

    if (q!=null){
        $.ajax({
            url: "https://perhalvorsen.com/radio/search",
            data: {"query_str": q},
            success: function(data){
                var empty = $("results").html();
                $("#results").html(data);
            }
        });
    }
}
