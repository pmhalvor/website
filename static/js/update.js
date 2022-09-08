// UPDATE SCRIPT
var progressbar = document.getElementById("bar");

var duration = -1;  // -1 to make int not string
var progress = 0;
var percentage;
var timestep = 1000;

function updateProgress(){
    progress = progress + timestep;
    if(duration==0) {
        progress = 0;
        clearInterval(updating);
        return;
    }
    else if (progress<duration) {
        percentage = Math.round(100*progress/duration);
        $('.progressbar').css('width', percentage +"%");
        $('.progressbar').innerHTML = percentage +"%";
        return percentage;
    }
    else { // duration is not 0 and progress is greater than duration
        update('current');
        retrieve('recents');
        return;
    }
}

function current(json){
    var info = '';
    if(json.artist){
        info += json.artist+' - ';
    }
    info += json.track;

    if (json.track) {
        $("#playingArtist").html(json.artist);
        $("#playingTrack").html(json.track);
        $("#artwork").attr("src", json.artwork);
        progress = json.progress*1;
        duration = json.duration*1;
    }
}


var updating = setInterval(updateProgress, timestep);



