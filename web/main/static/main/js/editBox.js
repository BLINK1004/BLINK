var btnEdit = document.getElementById("edit");
var form = document.getElementById("json_data").textContent;
var ctx2;
var canvasMain = document.getElementById("canvas-main");
var objectList = document.getElementById("object-list");

var jsonForm = JSON.parse(form)
console.log("--------------JSON.parse(obj) result in EditBox ----------");
console.log(jsonForm);

        for(key in jsonForm){
            var form = document.createElement('form');
            objectList.appendChild(form);

            var div_kor = document.createElement('div');
            div_kor.classList.add('form-group');
            div_kor.innerText = jsonForm[key].txt;
            div_kor.setAttribute("contenteditable", "true");
            form.appendChild(div_kor);

            var text_label = document.createElement('input');
            text_label.type = 'text';
            text_label.classList.add('form-control');
            text_label.innerText = jsonForm[key].txt;
            div_kor.appendChild(text_label);

            console.log(jsonForm[key].x);
            var div = document.createElement('div');
            div.style.color = "black";
            div.innerText = jsonForm[key].txt;
            div.style.left = jsonForm[key].x +"px";
            div.style.top = jsonForm[key].y +"px";
            div.style.width = jsonForm[key].w +"px";
            div.style.height = jsonForm[key].h + "px";
            div.setAttribute("contenteditable", "true");
            div.style.overflow = "hidden";
            div.style.position = "absolute";
            canvasMain.appendChild(div);

        }
