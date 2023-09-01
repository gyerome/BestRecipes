var chunksQuantity = 0;
let isChunkLoading = false;

function loadChunk(loadUrl) {
    let data = `order_by=rating&chunks_quantity=${chunksQuantity}`;
    if (typeof curCategory == 'undefined') curCategory = null;
    if (typeof curFilter == 'undefined') curFilter = null;
    if (typeof curUser == 'undefined') curUser = null;
    if (typeof curType == 'undefined') curType = null;
    if (typeof curSearch == 'undefined') curSearch = null;
    if (curFilter!=null) data = data + `&order_by=${curFilter}`;
    if (curCategory!=null) data = data + `&category=${curCategory}`;
    if (curUser!=null) data = data + `&user=${curUser}`;
    if (curType!=null) data = data + `&type=${curType}`;
    if (curSearch!=null) data = data + `&search=${curSearch}`;
    $.get({
        url: loadUrl,
        data: data,
        dataType: 'html',
        success: function(data){
                document.getElementById('content').insertAdjacentHTML('beforeend', data);
                chunksQuantity++;
                isChunkLoading=false;
                return true;
        },
        error: function(jqXhr, textStatus, errorThrown) {
        isChunkLoading = false;
        return false;
        }
    })
}

function populate() {
    let errorTriesQuantity = 0;
    while(true) {
        let windowRelativeBottom = document.getElementById("content").getBoundingClientRect().bottom;
        if (windowRelativeBottom > document.documentElement.clientHeight + 50) break;
        if (!isChunkLoading) break;
        isChunkLoading = true;
        LoadingSuccess = loadChunk();
        if (!LoadingSuccess) errorTriesQuantity++;
        if (errorTriesQuantity>=3) break;
    }
}
window.addEventListener('scroll', populate);
loadChunk(loadUrl);