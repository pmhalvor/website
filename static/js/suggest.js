// SUGGEST SCRIPT
// handling search bar data
$("#table tr").click(function(){
    var artist = $(this).find("#artist").html();
    var track = $(this).find("#track").html();
    var id = this.id;
    var dt = new Date();
    var time = `${dt.getUTCFullYear()}-${dt.getUTCMonth() + 1}-${dt.getUTCDate()} ${dt.getHours()}:${dt.getMinutes()}:${dt.getSeconds()}`;
    if (idRecommended(id)){
        removeRecommendation(id);
    }else{
        addRecommendation(artist, id, time, track);
    }
});

function addRecommendation(artist, id, time, track){
    $("#recommendations").append("<tr class='recommended' id='"+id+"'><td id='artist'>"+artist+"</td><td id='track'>"+track+"</td><td id='time'>"+time+"</td></tr>");
}

function removeRecommendation(id){
    $("#recommendations").find("#"+id).remove();
}

function idRecommended(id){
    var row = $("#recommendations").find("#"+id).html();
    if (row!=null){
        return true;
    }
    return false;
}
