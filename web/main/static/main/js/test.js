var ctx2;
var canvasMain = document.getElementById("selectable");
var objectList = document.getElementById("object-list");

var form = document.getElementById("json_data").textContent;
var jsonForm = JSON.parse(form)
console.log("--------------JSON.parse(obj) result in EditBox ----------");
console.log(jsonForm);

var bubbleList = document.querySelector(".js-bubbleList");
var BUBBLES_LS = "bubbles";

//json 내 제거하고자 하는 말풍선 데이터 삭제
function deleteJson(id){
    delete jsonForm[id];
    console.log(jsonForm);
    document.getElementById("json_data").innerText = JSON.stringify(jsonForm);
    console.log(document.getElementById("json_data").innerText);
}

//화면 오른쪽에서 해당 리스트 삭제
function deleteBox(id){
    var name2 = 'div ' + id;
    var child = document.getElementById(name2);
    child.remove();
    }

//delete버튼을 누를 때 얻은 event로 target을 찾아 제거
function deleteBubble(event){
    var btn = event.target;
    var li = btn.parentNode;
    bubbleList.removeChild(li);
    deleteBox(li.id);
    deleteJson(li.id);
}

function inputBubble(event){
    var btn = event.target;
    var li = btn.parentNode;
    console.log(jsonForm[li.id])
    var canvas = document.getElementById("canvas-main");
    var div_img = document.createElement('img');
    div_img.id = 'div_img'
    div_img.src = "http://127.0.0.1:8000/media/main/20/06/gen_1.png";
    div_img.style.left = jsonForm[li.id].x +"px";
    div_img.style.top = jsonForm[li.id].y +"px";
    div_img.style.width = "64px";
    div_img.style.height = "64px";
    div_img.style.overflow = "hidden";
    div_img.style.position = "absolute";
    canvas.appendChild(div_img);
}

//화면 오른쪽에 원본 txt와 번역 txt를 나열해주고 잘못된 말풍선을 지울 수 있도록 설정
function showBubbleList(){
    for(key in jsonForm){
    var li = document.createElement("li");
    li.id = key;

    var div_kor = document.createElement('div');
    div_kor.classList.add('form-group');
    div_kor.value = jsonForm[key].txt;
    div_kor.innerText = jsonForm[key].txt;
    div_kor.setAttribute("contenteditable", "false");
    li.appendChild(div_kor);

    var delete_button = document.createElement('button');
    delete_button.classList.add('delbutton');
    delete_button.innerText = "Del";
    delete_button.addEventListener("click", deleteBubble);
    li.appendChild(delete_button);

    var input_button = document.createElement('button');
    input_button.classList.add('inpbutton');
    input_button.innerText = "input";
    input_button.addEventListener("click", inputBubble);
    li.appendChild(input_button);

    //          영어 번역 결과가 들어가는 txt
    var text_label = document.createElement('div');
    text_label.classList.add('form-control');
    text_label.value = jsonForm[key].t_txt;
    text_label.innerText = jsonForm[key].t_txt;
    text_label.setAttribute("contenteditable", "true");
    li.appendChild(text_label);
//    var text_label = document.createElement('input');
//    text_label.type = 'text';
//    text_label.classList.add('form-control');
//    text_label.innerText = jsonForm[key].t_txt;
//    li.appendChild(text_label);

    bubbleList.appendChild(li);
    }
}

//canvas(만화) 위에 사용자가 지정한 영역에 번역 결과를 띄워줌
function paintBubbles(){
    for(key in jsonForm){
        var div = document.createElement('div');
        div.classList.add('bubble');
        div.classList.add(key);
        div.classList.add("ui-widget-content");
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
        div_txt.id = 'div ' + key;
        div_txt.style.color = "black";
        div_txt.innerText = jsonForm[key].t_txt;
        div_txt.style.left = jsonForm[key].center[1];
        div_txt.style.top = jsonForm[key].center[0];
        div_txt.setAttribute("contenteditable", "true");
        div_txt.style.textAlign = "center";
        div_txt.style.verticalAlign = "middle";
        div_txt.style.position = "relative";
        div_txt.style.display = "table-cell";
        div_txt.style.fontSize = jsonForm[key].fontSize;
        div_txt.style.fontFamily = jsonForm[key].font;
        console.log(jsonForm[key].font);
        div.appendChild(div_txt);
    }
    }

//paintBubbles()와 showBubbleList() 함수 실행
function init(){
    paintBubbles();
    showBubbleList();

}

//동작 시작
init();

//$(".bubble").draggable({      // 드래그
//    cursor:"move",      // 드래그 시 커서모양
//    stack:".post",      // .post 클래스끼리의 스택 기능
//    opacity:0.8         // 드래그 시 투명도
//});

$(".bubble").bind("dragstart",function(event, ui){
    $(this).addClass("color");  //bgi 체인지

    //움직일 때 변경된 좌표를 json에 다시 저장
    var x = $(this).position().left;
    var y = $(this).position().top;
    var w = $(this).position().width;
    var h = $(this).position().height;

    var id = $(this).attr("id");

    jsonForm[id].x = x;
    jsonForm[id].y = y;
    jsonForm[id].w = w;
    jsonForm[id].h = h;

    console.log(jsonForm);

});

$(".bubble").bind("dragstop", function(event, ui){
    $(this).removeClass("color");   //bgi 체인지
});

//Metal Mania 글씨체 변경
$(".MetalMania").bind("click", function(event, ui){
    $("#selectable").find('div.ui-selected').find('div').css('font-family', 'Metal Mania');
});

//ArchitectsDaughter 글씨체 변경
$(".ArchitectsDaughter").bind("click", function(event, ui){
    $("#selectable").find('div.ui-selected').find('div').css('font-family', 'Architects Daughter');
});
$(".OpenSans").bind("click", function(event, ui){
    $("#selectable").find('div.ui-selected').find('div').css('font-family', 'Open Sans');
});

//글자 크기 증가
$("#font-plus").bind("click", function(event, ui){
//    $("#selectable").find('div.ui-selected').find('div').css('font-size', 'Architects Daughter');
     $speech = $("#selectable").find('div.ui-selected').find('div');
     var currentSize = $speech.css("fontSize");
     var num = parseFloat(currentSize, 10);
     var unit = currentSize.slice(-2);

     num += 1;

     $speech.css("fontSize", num+unit);

});

//글자 크기 감소
$("#font-minus").bind("click", function(event, ui){
//    $("#selectable").find('div.ui-selected').find('div').css('font-size', 'Architects Daughter');
     $speech = $("#selectable").find('div.ui-selected').find('div');
     var currentSize = $speech.css("fontSize");
     var num = parseFloat(currentSize, 10);
     var unit = currentSize.slice(-2);
     num -= 1;
     $speech.css("fontSize", num+unit);
});

//form-control text 변경 감지
$("body").on('propertychange change keyup paste input', ".form-control", function(event) {
    var btn = event.target;
    var li = btn.parentNode;

    var div = 'div ' + li.id;
    var divbox = document.getElementById(div);
    divbox.innerText = btn.innerText;
    jsonForm[li.id].t_txt = btn.innerText;
    document.getElementById("json_data").innerText = JSON.stringify(jsonForm);
});

