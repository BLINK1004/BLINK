var btnEdit = document.getElementById("edit");
var form = document.getElementById("form-path").textContent;
var ctx2;

   btnEdit.onclick = function(e) {
        var a = JSON.parse(form)
        var jsonForm = JSON.parse(a)
        console.log("--------------JSON.parse(obj) result in EditBox ----------");
        console.log(jsonForm);

        for(key in jsonForm.path){
         console.log(jsonForm.path[key].x);
         x = jsonForm.path[key].x;
         y = jsonForm.path[key].y;
         w = jsonForm.path[key].width;
         h = jsonForm.path[key].height;

            canvas = document.getElementById("canvas");
            if (canvas == null || canvas.getContext == null) return;
            ctx2 = canvas.getContext("2d");
            ctx2.strokeStyle = "red";
            ctx2.lineWidth = 10;
            color = "rgba(255, 255, 255, 0)"
            ctx2.fillStyle = color;
            ctx2.fillRect(x, y, w, h);
            ctx2.strokeRect(x, y, w, h);
        }
   }