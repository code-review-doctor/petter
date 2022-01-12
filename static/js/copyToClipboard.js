let CopyToClipBoard = function (element_id) {
    let text_element = document.getElementById(element_id)
    let text = text_element.value
    if (navigator.clipboard != undefined) {//Chrome
        navigator.clipboard.writeText(text).then(function () {
            text_element.select()
            text_element.title = 'Skopiowano do schowka'
        }, function (err) {
            console.error('Could not copy text: ', err);
        });
    } else if (window.clipboardData) { // Internet Explorer
        window.clipboardData.setData("Text", text);
    }
};
