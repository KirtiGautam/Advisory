function SlideMenu() {
    if (document.getElementById('menu').style.width == '250px') {
        document.getElementById('menu').style.width = '0';
        document.getElementById('content').style.marginLeft = '0';
    }

    else {
        document.getElementById('menu').style.width = '250px';
        document.getElementById('content').style.marginLeft = '250px';
    }
}

function closeSlideMenu() {
    document.getElementById('menu').style.width = '0';
    document.getElementById('content').style.marginLeft = '0';
}
