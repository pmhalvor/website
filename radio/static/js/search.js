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
    $("#results").html("<tr><td style='background-color:black'></td><td style='background-color:black'><img style='width:180px;height:100px' src='../static/img/loading.gif' id='loading'></td></tr>");
}

function searchSpotify(q){

    if (q!=null){
        $.ajax({
            async: true,
            url: "search",
            data: {"query_str": q},
            success: function(data){
                $("#results").html(data);
                $("#results").append('<script src="../static/js/suggest.js" type="text/javascript" name="suggest"></script>');
            },
        });
    }
}
