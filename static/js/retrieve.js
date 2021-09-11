function retrieve(section)
{
    $.ajax({
        url : '/radio/'+section,
        type: 'GET',
        success: function(data){
            var sectionDiv = $('.'+section);
            var position = sectionDiv.scrollLeft();
            sectionDiv.html(data);
            sectionDiv.scrollLeft(position);
        }
    });

}


function update(section) {
    $.ajax({
        url : '/radio/update/'+section,
        success: function(data){
            if (data.failed){
                console.log(data.data);
            }
            else if (section=="current"){
                current(data.current);
            }
        }, 

    })
}




