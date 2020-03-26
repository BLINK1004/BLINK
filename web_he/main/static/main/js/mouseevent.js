var WinDrag = function(layer) { 
    var isFirstMove = true;
    WinDrag.selectedLayer = layer;
    layer.style.position = "absolute";
    layer.onmousedown = onDragStart;
    layer.setAttribute("isOnDragging", "false");
    document.onmousemove = onDragging;
    document.onmouseup = onDragStop;

        function getWindowWidth() {
            var width = 0;
            if( typeof( window.innerWidth ) == 'number' ) {
            //Non-IE width = window.innerWidth;
            } else if( document.documentElement && ( document.documentElement.clientWidth) ) {
            //IE 6+ in 'standards compliant mode'
            width = document.documentElement.clientWidth;
            } else if( document.body && ( document.body.clientWidth) ) {
            //IE 4 compatible
            width = document.body.clientWidth;
        }
        console.log(width);
        return width;
        }

        function getWindowHeight() {
            var height = 0;
            if( typeof( window.innerWidth ) == 'number' ) {
            //Non-IE
            height = window.innerHeight;
            } else if( document.documentElement && (document.documentElement.clientHeight) ) {
            //IE 6+ in 'standards compliant mode'
            height = document.documentElement.clientHeight;
            } else if( document.body && (document.body.clientHeight ) ) { //IE 4 compatible height = document.body.clientHeight;
            }
            console.log(height);
            return height;
        }

        function onDragStart() {
         WinDrag.selectedLayer = this;
        WinDrag.selectedLayer.setAttribute("isOnDragging", "true");
        }

        function onDragStop() {
        isFirstMove = true;
        WinDrag.selectedLayer.setAttribute("isOnDragging", "false"); }

        function onDragging(e) {
         if(WinDrag.selectedLayer.getAttribute("isOnDragging") == "false") { return; }
        var mouse = document.all ? event : e;

        if(isFirstMove == true) {
        WinDrag.selectedLayer.setAttribute("orgX", mouse.clientX - WinDrag.selectedLayer.offsetLeft);
        WinDrag.selectedLayer.setAttribute("orgY", mouse.clientY - WinDrag.selectedLayer.offsetTop);
        isFirstMove = false;
        }

        var left = mouse.clientX - WinDrag.selectedLayer.getAttribute("orgX");
        var top = mouse.clientY - WinDrag.selectedLayer.getAttribute("orgY");
        WinDrag.selectedLayer.style.top = (top >= 0 ? (top + WinDrag.selectedLayer.clientHeight >= getWindowHeight() ? getWindowHeight() - WinDrag.selectedLayer.clientHeight : top) : 0) + "px";
        WinDrag.selectedLayer.style.left = (left >= 0 ? (left + WinDrag.selectedLayer.clientWidth >= getWindowWidth() ? getWindowWidth() - WinDrag.selectedLayer.clientWidth : left) : 0) + "px"; } }