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