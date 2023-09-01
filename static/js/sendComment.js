$('#comment-form').submit(function (){
    $.post(
        '/api/newcomment',
        $('#comment-form').serialize()
        //loadChunk()
    )
}
)