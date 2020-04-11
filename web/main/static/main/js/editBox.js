   var btnEdit = document.getElementById("edit");
   var form = document.getElementById("form-path").textContent;
   btnEdit.onclick = function(e) {
        var a = JSON.parse(form)
        var jsonForm = JSON.parse(a)
        console.log("--------------JSON.parse(obj) result in EditBox ----------");
        console.log(jsonForm);

        for(key in jsonForm.path){
        console.log(jsonForm.path[key].x);
        }
   }