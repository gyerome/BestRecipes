function login() {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.post({
        url: '/user/auth',
        data: {
            username: document.getElementById('ident').value,
            password: document.getElementById('password').value,
            csrfmiddlewaretoken: csrf,
        },
        success: function(response) {
            content = document.getElementById('content').innerHTML;
            document.documentElement.innerHTML = response;
            document.getElementById('content').innerHTML = content;
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            container = document.getElementById('shadow-container');
            container.innerHTML = '';
            container.id = '';
            container.innerHTML = XMLHttpRequest.responseText;
            },
    })
}