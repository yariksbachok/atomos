window.onload = function() {
  try{
    if (window.File && window.FileList && window.FileReader) {
      var filesInput = document.getElementById("uploadImage");
      filesInput.addEventListener("change", function(event) {
        var files = event.target.files;
        var output = document.getElementById("result");
        for (var i = 0; i < files.length; i++) {
          var file = files[i];
          if (!file.type.match('image'))
            continue;
          var picReader = new FileReader();
          picReader.addEventListener("load", function(event) {
            var picFile = event.target;
            var div = document.createElement("div");
            div.innerHTML = "<img class='thumbnail' src='" + picFile.result + "'" +
              "alt='" + picFile.name + "'/>";
            output.insertBefore(div, null);
          });
          picReader.readAsDataURL(file);
        }

      });
    }
  }catch{

  }
}


function likeToggler(e, id){
    const paths = e.children;
    const f_each = Array.prototype.forEach.bind(paths) 
    const count_of_likes = e.parentNode.parentNode.querySelector("p");
    fetch(`${window.location.protocol}/addLike?post_id=${id}`);
    if( paths[0].classList.contains('like_active') != true){
        f_each( p => p.classList.add('like_active'))
 
        count_of_likes.innerText = +count_of_likes.innerText + 1
    }
        else{
        f_each( p => p.classList.remove('like_active'))
        count_of_likes.innerText = +count_of_likes.innerText - 1
    }
}


function copy(e){
    const comment_area = e.parentNode.parentNode.parentNode.querySelector(".content_comment p")
    navigator.clipboard.writeText(comment_area.innerText)
}

(function(){
  try{
      var textarea = document.querySelector('.form_for_comment p textarea'); 
      textarea.addEventListener('keyup', 
      function(){
          if(this.scrollTop > 0){
                this.style.height = this.scrollHeight + "px";
          } 
      });
  }catch{

  }
})()





const textarea = document.querySelector( '.form_for_comment form p textarea');



try{
  textarea.addEventListener( 'keyup', (e) => {
      if( e.key != 'Enter' && e.target.value ){
          return
      }

      if(e.ctrlKey || e.shiftKey){
          e.target.value += '\n'
          console.log(e.ctrlKey)
          return
      }
      const onclick_string = document.querySelector('.input_in_add input').attributes.onClick.value;
      const user_id_arr = onclick_string.split("(")[1].split("");
      user_id_arr.pop();
      const user_id = user_id_arr.join("");


      // if( e.target.value === "\n" || e.target.value === " "){
      //     e.target.value = ""
      // }

      
      // e.target.value=""
      
      
  })
}catch{

}