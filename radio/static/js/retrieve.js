function retrieve(section)
{
    $.ajax({
        url : '/radio/'+section,
        type: 'GET',
        success: function(data){
            $('.'+section).html(data);
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




