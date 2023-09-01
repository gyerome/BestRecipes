var curCategory = null;
var curFilter = null

function setFilter(filter) {
    document.getElementById('content').innerHTML = '';
    chunksQuantity = 0;
    curFilter = filter;
    loadChunk(loadUrl)
}

function setCategory(filter) {
    document.getElementById('content').innerHTML = '';
    chunksQuantity = 0;
    curCategory = filter;
    loadChunk(loadUrl)
}

function setType(filter) {
    document.getElementById('content').innerHTML = '';
    chunksQuantity = 0;
    curType = filter;
    loadChunk(loadUrl)
}