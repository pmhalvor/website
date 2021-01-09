// UPDATE SCRIPT
var progressbar = document.getElementById("bar");

var duration = "{{ current.duration }}"*1;  // *1 to make int not string
var progress = "{{ current.progress }}"*1;
var percentage;

function updateProgress(){
    progress = progress + 1000;
    if (duration==0){
        progress = 0;
        recents();
        return 0;
    }
    else if (progress<duration) {
        percentage = Math.round(100*progress/duration);
        progressbar.style.width = percentage +"%";
        progressbar.innerHTML = percentage +"%";
        return percentage;
    }
    else {
        current();
        recents();
    }
}

function current(){
    $.ajax({ // UPDATE NOW PLAYING
        url: "https://perhalvorsen.com/radio/current",
        success: function(json) {
            console.log(json.artist, '-', json.track);
            $("#playingArtist").html(json.artist);
            $("#playingTrack").html(json.track);
            $("#artwork").attr("src", json.artwork);
            progress = json.progress*1;
            duration = json.duration*1;
        }
    });
}
function recents(){
    $.ajax({ // UPDATE RECENTLY PLAYED 
            url: "https://perhalvorsen.com/radio/recents",
            success: function(data) {
                $("#recents").html(data);
            }
        });
}

var updating = setInterval(updateProgress, 1000);
