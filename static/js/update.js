// UPDATE SCRIPT
var progressbar = document.getElementById("bar");

var duration = -1;  // -1 to make int not string
var progress = 0;
var percentage;

function updateProgress(){
    progress = progress + 2000;
    if(duration==0) {
        progress = 0;
        clearInterval(updating);
        return;
    }
    else if (progress<duration) {
        percentage = Math.round(100*progress/duration);
        progressbar.style.width = percentage +"%";
        progressbar.innerHTML = percentage +"%";
        return percentage;
    }
    else { // duration is not 0 and progress is less than duration
        current();
        recents();
        return;
    }
}

function current(){
    $.ajax({ // UPDATE NOW PLAYING
        url: "current",
        success: function(json) {
            var info = '';
            if(json.artist){
                info += json.artist+' - ';
            }
            info += json.track;
            console.log(info);
            $("#playingArtist").html(json.artist);
            $("#playingTrack").html(json.track);
            $("#artwork").attr("src", json.artwork);
            progress = json.progress*1;
            duration = json.duration*1;
        },
    });
}
function recents(){
    $.ajax({ // UPDATE RECENTLY PLAYED 
            url: "recents",
            success: function(data, textStatus, xhr){
                if(xhr.status==200){
                    $("#recents").html(data);
                }
                else{
                    console.log(xhr.status);
                    console.log(textStatus);
                }
            }
        });
}

var updating = setInterval(updateProgress, 2000);



