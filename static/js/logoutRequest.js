function logOut() {
    $.post({
        url: '/logout',
        success: function () {location.reload();}
    })
}