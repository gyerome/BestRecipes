function subscribe(authorId, subscriberId, buttonId, csrf) {
    $.post({
        url: '/api/subscribe',
        data: {author_id: authorId,
               subscriber_id: subscriberId,
               csrfmiddlewaretoken: csrf},
        dataType: 'html',
        success: function(data) {
            let button = document.getElementById(buttonId);
            button.className = 'subscribe-button-active';
        }
    });
}