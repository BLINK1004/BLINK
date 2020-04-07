         var canvas;
         var ctx;
         var arRectangle = new Array();
         var sx, sy;                  // 드래그 시작점
         var ex, ey;                  // 드래그 끝점
         var color;               // 현재 색상
         var drawing;                // 그리고 있는 중인가
         var moving = -1;              // 이동중인 도형 첨자


         // 사각형 생성자
         function Rectangle(sx, sy, ex, ey, color) {
              this.sx = sx;
              this.sy = sy;
              this.ex = ex;
              this.ey = ey;
              this.color = color;
         }

         function getRectangle(x, y) {
              for (var i = 0;i < arRectangle.length;i++) {
                   var rect = arRectangle[i];
                   if (x > rect.sx && x < rect.ex && y > rect.sy && y < rect.ey) {
                        return i;
                   }
              }
              return -1;
         }

         // 화면 지우고 모든 도형을 순서대로 다 그림
         function drawRects() {
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              for (var i = 0;i < arRectangle.length;i++) {
                   var r = arRectangle[i];
                   ctx.fillStyle = r.color;
                   ctx.fillRect(r.sx, r.sy, r.ex-r.sx, r.ey-r.sy);
                   ctx.strokeRect(r.sx, r.sy, r.ex-r.sx, r.ey-r.sy);
              }
         }

         window.onload = function() {
              canvas = document.getElementById("canvas");
              if (canvas == null || canvas.getContext == null) return;
              ctx = canvas.getContext("2d");
              ctx.strokeStyle = "black";
              ctx.lineWidth = 2;
              color = "rgba(255, 255, 255, 0)"
              ctx.fillStyle = color;

              canvas.onmousedown = function(e) {
                   e.preventDefault();

                   // 클릭한 좌표 구하고 그 위치에 도형이 있는지 조사
                   sx = canvasX(e.clientX);
                   sy = canvasY(e.clientY);
                   moving = getRectangle(sx, sy);

                   // 도형을 클릭한 것이 아니면 그리기 시작
                   if (moving == -1) {
                        drawing = true;
                   }
              }

              canvas.onmousemove = function(e) {
                   e.preventDefault();
                   ex = canvasX(e.clientX);
                   ey = canvasY(e.clientY);

                   // 화면 다시 그리고 현재 도형 그림
                   if (drawing) {
                        drawRects();
                        ctx.fillStyle = color;
                        ctx.fillRect(sx, sy, ex-sx, ey-sy);
                        ctx.strokeRect(sx, sy, ex-sx, ey-sy);
                   }

                  // 상대적인 마우스 이동 거리만큼 도형 이동
                   if (moving != -1) {
                        var r = arRectangle[moving];
                        r.sx += (ex - sx);
                        r.sy += (ey - sy);
                        r.ex += (ex - sx);
                        r.ey += (ey - sy);
                        sx = ex;
                        sy = ey;
                        drawRects();
                   }
              }

              canvas.onmouseup = function(e) {
                   // 좌표 정규화해서 새로운 도형을 배열에 추가
                   if (drawing) {
                        var x1 = Math.min(sx, ex);
                        var y1 = Math.min(sy, ey);
                        var x2 = Math.max(sx, ex);
                        var y2 = Math.max(sy, ey);

                        arRectangle.push(new Rectangle(x1, y1, x2, y2,color));
                   }
                    console.log("x: " + sx + "y: " + sy + "width: " + (ex-sx) + "height: " + (ey-sy))
                   drawing = false;
                   moving = -1;
              }
         }

         var selcolor = document.getElementById("selcolor");
<!--         selcolor.onchange = function(e) {-->
<!--              color = selcolor.value;-->
<!--         }-->

         var btnclear = document.getElementById("clear");
         btnclear.onclick = function(e) {
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              arRectangle.length = 0;
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
