var curSearch = null;
function search() {
    curSearch = document.getElementById('search').value;
    if (curSearch == '') curSearch = null;
    document.getElementById('content').innerHTML = '';
    chunksQuantity = 0;
    loadChunk(loadUrl);
}