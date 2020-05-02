var btnEdit = document.getElementById("edit");
var form = document.getElementById("json_data").textContent;
var ctx2;

        var jsonForm = JSON.parse(form)
        console.log("--------------JSON.parse(obj) result in EditBox ----------");
        console.log(jsonForm);

        for(key in jsonForm){
            console.log(jsonForm[key].x);
            var canvasMain = document.getElementById("canvas-main");
            var div = document.createElement('div');
            div.style.color = "red";
            div.innerText = key;
            div.style.left = jsonForm[key].x +"px";
            div.style.top = jsonForm[key].y +"px";
            div.style.width = jsonForm[key].w +"px";
            div.style.height = jsonForm[key].h + "px";
            div.style.border = "2px solid black";
            div.style.background="blue";
            div.style.overflow = "hidden";
            div.style.position = "absolute";
            canvasMain.appendChild(div);
        }
