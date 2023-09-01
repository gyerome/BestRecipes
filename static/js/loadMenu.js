function loadMenu(pageUrl) {
    $.ajax({
        url: pageUrl,
        method: 'get',
        dataType: 'html',
        success: function(data){
            document.body.insertAdjacentHTML('beforebegin',data);
            document.addEventListener("keydown", deleteMenu);
        }
    });
}

function deleteMenu(e) {
    if (e.code == "Escape") {
        document.getElementById('shadow-container').remove();
        document.removeEventListener('keydown', deleteMenu);
    }

}

