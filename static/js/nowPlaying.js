var progressbar = document.getElementById("bar");

var duration = "{{ current.duration }}"*1;
var progress = "{{ current.progress }}"*1;
var percentage;

function updateProgress(){
    progress = progress + 1000;
    if (duration==0){
        // do nothing
        return;
    }
    else if (progress<duration) {
        percentage = Math.round(100*progress/duration);
        progressbar.style.width = percentage +"%";
        progressbar.innerHTML = percentage +"%";
        return percentage;
    }
    else {
        // location.reload(true);
        var playingArtist = document.getElementById("playingArtist");
        var playingTrack = document.getElementById("playingTrack");
        var artwork = document.getElementById("artwork");
        playingArtist.innerHTML = "Refresh page for next song";
        playingTrack.innerHTML  = "(CTRL + F5)";
        artwork.src = "https://perhalvorsen.com/media/img/empty_album.png";
        clearInterval(updating);
    }
}

var updating = setInterval(updateProgress, 1000);
