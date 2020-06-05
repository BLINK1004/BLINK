var canvas;
var ctx;
var arRectangle = new Array();
var sx, sy;                  // 드래그 시작점
var ex, ey;                  // 드래그 끝점
var angle;
var color;               // 현재 색상
var is_drawing;                // 그리고 있는 중인가
var is_moving = -1;              // 이동중인 도형 첨자
var is_rotate = -1; // 박스 회전 이벤트
var is_extend = -1; // 박스 확장 이벤트
var jsonArray = new Array();
var json = new Object();
var totalJson = new Object();
var qx, qy;
var extend_points = new Array();


// 사각형 생성자
function Rectangle(sx, sy, ex, ey, angle, color, rx, ry, extend_points) {
    this.sx = sx;
    this.sy = sy;
    this.ex = ex;
    this.ey = ey;
    this.angle = angle;
    this.color = color;
    this.rx = rx;
    this.ry = ry;
    this.extend_points = extend_points;
}

function getMovePoint(x, y) {
    for (var i = 0;i < arRectangle.length;i++) {
         var rect = arRectangle[i];
         if (x > rect.sx && x < rect.ex && y > rect.sy && y < rect.ey) {
              return i;
         }
    }
    return -1;
}

function getRotatePoint(x, y) {
    for (var i = 0;i < arRectangle.length;i++) {
         var rect = arRectangle[i];
         console.log("상자 :" + rect.rx + " : " + rect.ry)
         console.log("마우스 :" + x + " : " + y)
         if (x > rect.rx-10 && x < rect.rx+10 && y > rect.ry-10 && y < rect.ry+10) {
              return i;
         }
    }
    return -1;
}

function getExtendPoint(x, y) {
    for (var i = 0;i < arRectangle.length;i++) {
         var rect = arRectangle[i];

         for (var j = 0; j < rect.extend_points.length; j++) {
            console.log('포인트 통과! ' + i + rect.extend_points.length)

            center_x = rect.extend_points[j][0]
            center_y = rect.extend_points[j][1]
            console.log('center_x ' + center_x)
            console.log('x ' + x)

            if (x > center_x-10 && x < center_x+10 && y > center_y-10 && y < center_y+10) {

              return i;
            }

         }

    }
    return -1;
}

// 화면 지우고 모든 도형을 순서대로 다 그림
function drawRects() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0;i < arRectangle.length;i++) {
         var r = arRectangle[i];
         rotateRect(r, r.angle);
         draw_point(r);
    }
}

function rotateRect(r, angle) {
    //ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(255, 255, 255, 0)";

    ctx.save();

    ctx.translate(r.sx+(r.ex-r.sx)/2, r.sy+(r.ey-r.sy)/2 );
    ctx.rotate(angle*Math.PI/180);
    ctx.translate( -(r.sx + (r.ex-r.sx)/2), -(r.sy+ (r.ey-r.sy)/2) );
    ctx.fillRect(r.sx, r.sy, r.ex-r.sx, r.ey-r.sy);
    ctx.strokeRect(r.sx, r.sy, r.ex-r.sx, r.ey-r.sy);

    ctx.restore();
}

function draw_point(r){
    var epss = new Array([r.sx,r.sy],[r.ex,r.ey],[r.sx + (r.ex-r.sx), r.sy], [r.sx, r.sy + (r.ey-r.sy)]);
    var c_x = r.sx + ((r.ex-r.sx)/2);
    var c_y = r.sy + (r.ey-r.sy)/2;

    // 왼위, 왼아래, 오른위, 오른아래 점 그리기
    for (var i = 0;i < epss.length; i++) {

        var epx = epss[i][0];
        var epy = epss[i][1];

        var eqx = c_x + (Math.cos(r.angle*Math.PI/180) * (epx - c_x)) - (Math.sin(r.angle*Math.PI/180) * (epy - c_y));
        var eqy = c_y + (Math.sin(r.angle*Math.PI/180) * (epx - c_x)) + (Math.cos(r.angle*Math.PI/180) * (epy - c_y));

        r.extend_points[i][0] = eqx;
        r.extend_points[i][1] = eqy;

        ctx.fillRect(eqx-5, eqy-5, 10, 10);
        ctx.strokeRect(eqx-5, eqy-5, 10, 10);
    }

    // rotate 점 그리기
    var o_x = r.sx + (r.ex-r.sx)/2;
    var o_y = r.sy - 50;

    qx = c_x + (Math.cos(r.angle*Math.PI/180) * (o_x - c_x)) - (Math.sin(r.angle*Math.PI/180) * (o_y - c_y));
    qy = c_y + (Math.sin(r.angle*Math.PI/180) * (o_x - c_x)) + (Math.cos(r.angle*Math.PI/180) * (o_y - c_y));

    r.rx = qx;
    r.ry = qy;

    ctx.fillRect(qx-5, qy-5, 10, 10);
    ctx.strokeRect(qx-5, qy-5, 10, 10);

}


window.onload = function() {
    canvas = document.getElementById("canvas");
    if (canvas == null || canvas.getContext == null) return;
    ctx = canvas.getContext("2d");
    ctx.strokeStyle = "black";
    ctx.lineWidth = 4;
    color = "rgba(255, 255, 255, 0)"
    ctx.fillStyle = color;


//                var img = new Image();
//                img.src = "http://www.sporbiz.co.kr/news/photo/201506/4115_6180_2410.jpg";
//                img.onload = function(e){
//                    ctx.drawImage(img, 0,0);
//                }


   canvas.onmousedown = function(e) {
        e.preventDefault();

        // 클릭한 좌표 구하고 그 위치에 도형이 있는지 조사
        sx = canvasX(e.clientX);
        sy = canvasY(e.clientY);
        angle = 0;

        is_moving = getMovePoint(sx, sy);
        is_rotate = getRotatePoint(sx,sy);
        is_extend = getExtendPoint(sx,sy);

        // 도형을 클릭한 것이 아니면 그리기 시작
        if (is_moving == -1) {
            if(is_rotate == -1){
                if(is_extend== -1){
                    is_drawing = true;
                }
            }
        }

   }

   canvas.onmousemove = function(e) {
        e.preventDefault();
        ex = canvasX(e.clientX);
        ey = canvasY(e.clientY);

        // 화면 다시 그리고 현재 도형 그림
        if (is_drawing) {
             drawRects();
             ctx.fillStyle = color;
             ctx.fillRect(sx, sy, ex-sx, ey-sy);
             ctx.strokeRect(sx, sy, ex-sx, ey-sy);
        }

        // 상대적인 마우스 이동 거리만큼 도형 이동
        if (is_moving != -1) {
             var r = arRectangle[is_moving];
             r.sx += (ex - sx);
             r.sy += (ey - sy);

             r.ex += (ex - sx);
             r.ey += (ey - sy);

             r.rx += (ex - sx);
             r.ry += (ey - sy);

             for (var i = 0;i < r.extend_points.length;i++) {
                r.extend_points[i][0] += (ex - sx);
                r.extend_points[i][1] += (ey - sy);
             }

             drawRects();
             sx = ex;
             sy = ey;
        }

        // 마우스 위치따라 상자 회전
        if (is_rotate != -1) {
            var r = arRectangle[is_rotate];
            angle = parseInt((sx-ex)%180)
            r.angle = angle
            //rotateRect(r, angle)
            drawRects();
        }

        // 상자 확장
        if (is_extend != -1) {
            var r = arRectangle[is_extend];
            r.sx += (ex - sx);
            r.sy += (ey - sy);

            r.ex -= (ex - sx);
            r.ey -= (ey - sy);

            drawRects();
            sx = ex;
            sy = ey;
        }


   }

   canvas.onmouseup = function(e) {

        // 좌표 정규화해서 새로운 도형을 배열에 추가
        // 상자생성 끝났을때

        if (is_drawing) {
             var x1 = Math.min(sx, ex);
             var y1 = Math.min(sy, ey);
             var x2 = Math.max(sx, ex);
             var y2 = Math.max(sy, ey);

             var x3 = x1 + (x2-x1);
             var y3 = y1;

             var x4 = x1;
             var y4 = y1 + (y2-y1);

             qx = sx + (ex-sx)/2;
             qy = sy - 50;

             extend_points.push([x1,y1],[x2,y2],[x3,y3],[x4,y4]);

             arRectangle.push(new Rectangle(x1, y1, x2, y2, angle, color, qx, qy, extend_points));

             extend_points = new Array([]);
        }

        drawRects();

        var jsonArray = new Array();
        for (var i = 0; i < arRectangle.length; i++) {
            var json = new Object();
            json.x = arRectangle[i].sx;
            json.y = arRectangle[i].sy;
            json.width = (arRectangle[i].ex - arRectangle[i].sx);
            json.height = (arRectangle[i].ey - arRectangle[i].sy);
            //json.angle = arRectangle[i].angle;
            jsonArray.push(json);
        }

         //path 정보인 json이 담긴 array jsonArray를 담을 것임
         totalJson.path = jsonArray;
         var jsonInfo = JSON.stringify(totalJson);

         console.log("---------totaljson-------------")
         console.log(totalJson);


         is_drawing = false;
         is_moving = -1;
         is_rotate = -1;
         is_extend = -1;
   }
}

      //     var selcolor = document.getElementById("selcolor");
 // <!--         selcolor.onchange = function(e) {-->
 // <!--              color = selcolor.value;-->
 // <!--         }-->

var btnClear = document.getElementById("clear");
btnClear.onclick = function(e) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    arRectangle.length = 0;
    location.reload(true);
}

var btnSave = document.getElementById("trysave");
var pTag = document.getElementById("id_input_history")
btnSave.onclick = function(e){
pTag.innerText = JSON.stringify(totalJson);
}


function canvasX(clientX) {
    var bound = canvas.getBoundingClientRect();
    var bw = 5;
    return (clientX - bound.left - bw) * (canvas.width / (bound.width - bw * 2));
}

function canvasY(clientY) {
    var bound = canvas.getBoundingClientRect();
    var bw = 5;
    return (clientY - bound.top - bw) * (canvas.height / (bound.height - bw * 2));
}

