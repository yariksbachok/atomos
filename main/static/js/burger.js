function activete_burger(){
    console.log('123')
    var element = document.querySelector(".main_burger");
    element.classList.toggle("activeete");
    if(document.querySelector(".main_burger.activeete")){
        var burger = document.querySelector(".main_bur");
        burger.style.display='none'
        var burger_back = document.querySelector(".main_bur_none");
        burger_back.style.display='block'
    }else{
        var burger = document.querySelector(".main_bur");
        burger.style.display='block'
        var burger_back = document.querySelector(".main_bur_none");
        burger_back.style.display='none'
    }
}


var slideindex = 1
function plus_slide(n){
    show_slide(slideindex+=n)
}
function current_slide(n){
    if(slideindex == 1){
        slideindex = 0
    }
    show_slide(slideindex -= n)
}

function show_slide(n_slide){
    var slades = document.getElementsByClassName("quest_blocks_mobile")
    var new_slide = slades.length - 2
    if(n_slide == -1){
        n_slide = 4
        slideindex = 4
    }
    if(n_slide == 5){
        n_slide = 1
        slideindex = 1
    }
    if(n_slide == 1){
        var first = document.querySelector(".block_mobile__1");
        first.style.display = 'block'
        var second = document.querySelector(".block_mobile__2");
        second.style.display = 'none'
        var three = document.querySelector(".block_mobile__3");
        three.style.display = 'none'
        var four = document.querySelector(".block_mobile__4");
        four.style.display = 'none'
    }
    if(n_slide == 2){
        var first = document.querySelector(".block_mobile__1");
        first.style.display = 'none'
        var second = document.querySelector(".block_mobile__2");
        second.style.display = 'block'
        var three = document.querySelector(".block_mobile__3");
        three.style.display = 'none'
        var four = document.querySelector(".block_mobile__4");
        four.style.display = 'none'
    }
    if(n_slide == 3){
        var first = document.querySelector(".block_mobile__1");
        first.style.display = 'none'
        var second = document.querySelector(".block_mobile__2");
        second.style.display = 'none'
        var three = document.querySelector(".block_mobile__3");
        three.style.display = 'block'
        var four = document.querySelector(".block_mobile__4");
        four.style.display = 'none'
    }
    if(n_slide == 4){
        var first = document.querySelector(".block_mobile__1");
        first.style.display = 'none'
        var second = document.querySelector(".block_mobile__2");
        second.style.display = 'none'
        var three = document.querySelector(".block_mobile__3");
        three.style.display = 'none'
        var four = document.querySelector(".block_mobile__4");
        four.style.display = 'block'
    }
}