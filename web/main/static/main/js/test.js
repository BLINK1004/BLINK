var ctx2;
var canvasMain = document.getElementById("canvas-main");
var objectList = document.getElementById("object-list");

var form = document.getElementById("json_data").textContent;
var jsonForm = JSON.parse(form)
console.log("--------------JSON.parse(obj) result in EditBox ----------");
console.log(jsonForm);

const bubbleList = document.querySelector(".js-bubbleList");
const BUBBLES_LS = "bubbles";

function deleteBox(id){
    console.log(id);
    const div = document.getElementsByClassName('bubble')[id];
    console.log(div);
    const parent = div.parentNode;

    console.log(parent);
    parent.removeChild(div);
}

function deleteBubble(event){
    const btn = event.target;
    const li = btn.parentNode;
    bubbleList.removeChild(li);
    deleteBox(li.id);
}

function showBubbleList(){
    for(key in jsonForm){
    const li = document.createElement("li");
    li.id = key;

    var div_kor = document.createElement('div');
    div_kor.classList.add('form-group');
    div_kor.innerText = jsonForm[key].txt;
    div_kor.setAttribute("contenteditable", "true");
    li.appendChild(div_kor);

    var delete_button = document.createElement('button');
    delete_button.classList.add('delbutton');
    delete_button.innerText = "Del";
    delete_button.addEventListener("click", deleteBubble);
    li.appendChild(delete_button);

    //          영어 번역 결과가 들어가는 txt
    var text_label = document.createElement('input');
    text_label.type = 'text';
    text_label.classList.add('form-control');
    text_label.innerText = jsonForm[key].txt;
    li.appendChild(text_label);

    bubbleList.appendChild(li);
    }
}

function paintBubbles(){
    for(key in jsonForm){
        var div = document.createElement('div');
        div.classList.add('bubble');
        div.id = key;
        div.style.left = jsonForm[key].x +"px";
        div.style.top = jsonForm[key].y +"px";
        div.style.width = jsonForm[key].w +"px";
        div.style.height = jsonForm[key].h + "px";
        div.style.overflow = "hidden";
        div.style.position = "absolute";
        div.style.display = "table";
        canvasMain.appendChild(div);

        var div_txt = document.createElement('div');
        div_txt.style.color = "black";
        div_txt.innerText = jsonForm[key].txt;
        div_txt.style.left = jsonForm[key].center[1];
        div_txt.style.top = jsonForm[key].center[0];
        div_txt.setAttribute("contenteditable", "true");
        div_txt.style.textAlign = "center";
        div_txt.style.verticalAlign = "middle";
        div_txt.style.position = "relative";
        div_txt.style.display = "table-cell";
        div.appendChild(div_txt);
    }
    }

function init(){
    paintBubbles();
    showBubbleList();

}

init();

$(".bubble").draggable({      // 드래그
    cursor:"move",      // 드래그 시 커서모양
    stack:".post",      // .post 클래스끼리의 스택 기능
    opacity:0.8         // 드래그 시 투명도
});

$(".bubble").bind("dragstart",function(event, ui){
    $(this).addClass("color");  //bgi 체인지
});
$(".bubble").bind("dragstop", function(event, ui){
    $(this).removeClass("color");   //bgi 체인지
});