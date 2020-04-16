function SlideMenu() {
    if (document.getElementById('menu').style.width == '200px') {
        document.getElementById('menu').style.width = '0';
        document.getElementById('content').style.marginLeft = '0';
        document.getElementById('content').style.width = '100%';
    }

    else {
        document.getElementById('menu').style.width = '200px';
        document.getElementById('content').style.marginLeft = '200px';
        document.getElementById('content').style.width = '85%';
    }
}