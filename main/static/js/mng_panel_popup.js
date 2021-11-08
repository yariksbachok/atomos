//  обработчик событий для всплытия попапа
// const btn = document.getElementById("mng_btn");
// try{
//     btn.addEventListener( 'click', (e) => {
//         const popup = document.getElementsByClassName("mng_panel_popup_container");
//         popup[0].classList.toggle("show")
//     })
// }catch{

// }
//  обработчик событий для скрытия попапа(бэкграунд)
// const popup_container = document.getElementsByClassName("mng_panel_popup_container");
// popup_container[0].addEventListener('click', (e) => {
//     e.stopPropagation()
//     e.target.classList.remove('show');
// })
// //  обработчик событий для скрытия попапа(крестик)
// const cancel_popup_btn = document.getElementsByClassName('blue_chrest')
//     cancel_popup_btn[0].addEventListener('click', (e) => {
//     const popup = document.getElementsByClassName("mng_panel_popup_container");
//     popup[0].classList.remove('show');
// })
// // функция обработки попапа
// function func(id_popup,id_user) {
//     if(id_popup === 1){
//         const name = document.querySelector('#mng_popup_username');
//         name.innerHTML = "Vasya Pupkin"
//     }
// }
const message_sound = document.querySelector('#new_message_sound')
try{

    const ex_show_more_btn = document.querySelector('#exchange_show_more_btn')
    ex_show_more_btn.addEventListener('click', (event) => {
        const exchange_list = document.querySelector("#exchange_list")
        const profiles_count = exchange_list.children.length;
        const url = `${window.location.protocol}/exchange_show_more?count=${profiles_count}`
        fetch_data(url).then(
            (data) => {
                for(prof of data){
                    const new_elem = document.createElement('div')
                    new_elem.innerHTML = prof
                    exchange_list.append(new_elem)
                }
            }
        )
    })
}catch{

}

try{
    const search_show_more_btn = document.querySelector('#search_show_more')
    search_show_more_btn.addEventListener('click', (event) => {
        const search_list = document.querySelector("#search_list")
        const profiles_count = search_list.children.length;
        const url = `${window.location.protocol}/search_show_more?count=${profiles_count}`
        fetch_data(url).then(
            (data) => {
                for(prof of data){
                    const new_elem = document.createElement('div')
                    new_elem.innerHTML = prof
                    search_list.append(new_elem)
                }
            }
        )
    })
}catch{

}


async function fetch_data(url, options){
    const result = await fetch(url,{
        headers:{
            'Content-Type': 'application/json'
        }
    });
    return result.json();
}

function create_prof(profile){
    const profile_container = document.createElement('li')
    profile_container.classList.add('mng_list_elem')
    profile_container.innerHTML =
     `
        <span class="mng_user">
            <img src="main/static/img/svg/user_logo.svg" class="mng_user_logo">
            <div class="ib">
                <div class="search_user">
                    <a href="/profile/${profile.user.username}">
                        <span class="mng_name">${profile.user.first_name} ${profile.user.last_name}</span>
                    </a>
                </div>
            </div>
        </span>
        <span class="mng_btn_container">
        <span class="mng_cost">${profile.token_cost} $</span>
            <button class="registerbtn mng_btn hover_blue" id="mng_btn"
             onClick="show();fill_popup_buy(this, ${profile.user.id} )">Купить</button>
        </span>
    `
    return profile_container


}

function show_top_up(){
    const pp = document.querySelector(".mng_panel_popup_buy_container.tp_up")
    pp.classList.remove("no_show");
    pp.classList.add("show")
}


function show_found(elem) {
    const value = elem.value;
    const url = `${window.location.protocol}/search_profile?value=${value}`
    const search_list = document.querySelector("#search_list")
    const count = search_list.children.length;
    const show_more_btn = document.querySelector('#search_show_more')
    show_more_btn && show_more_btn.remove()
    for(let i= 0; i < count; i++){
        search_list.children[0].remove()
    }
     fetch_data(url).then(
            (data) => {

                for(prof of data){

                    const new_elem = document.createElement('div')
                    new_elem.innerHTML = prof
                    search_list.append(new_elem)
                }
            }
        )
}

show_found = debounce(show_found, 500)

function debounce(f, t) {
  return function (args) {
    let previousCall = this.lastCall;
    this.lastCall = Date.now();
    if (previousCall && ((this.lastCall - previousCall) <= t)) {
      clearTimeout(this.lastCallTimer);
    }
    this.lastCallTimer = setTimeout(() => f(args), t);
  }
}

const publications_show_more_btn = document.querySelector('#publications_show_more_btn')
publications_show_more_btn && publications_show_more_btn.addEventListener('click', (event) => {
    const publications_search_list = document.querySelector("#publications_search_list")
    const posts_count = publications_search_list.children.length;
    const url = `${window.location.protocol}/publications_show_more?count=${posts_count}`
    fetch_data(url).then(
        (data) => {
            for(post of data){
                const post_container = document.createElement('div')
                post_container.innerHTML = post
                publications_search_list.append(post_container)
            }
        }
    )
})


function show_found_posts(elem) {
    const value = elem.value;
    const url = `${window.location.protocol}/search_post?value=${value}`
    const publications_search_list = document.querySelector("#publications_search_list")
    const count = publications_search_list.children.length;
    const publications_show_more_btn = document.querySelector('#publications_show_more_btn')
    publications_show_more_btn && publications_show_more_btn.remove()
    for(let i= 0; i < count; i++){
        publications_search_list.children[0].remove()
    }
     fetch_data(url).then(
            (data) => {
                for(post of data){
                    const new_post = document.createElement('div')
                    new_post.innerHTML = post
                    publications_search_list.append(new_post)
                }
            }
        )
}

show_found_posts = debounce(show_found_posts, 500)

socket = new WebSocket(`ws://${window.location.host}/setOnline`)

const notificateSocket = new WebSocket(`ws://${window.location.host}/notifications`)

notificateSocket.onmessage=(data) => {
    const n_data = JSON.parse(data.data)
    let container = document.querySelector('.notification_container')
    if (!container) {
        container = document.createElement('div')
        container.classList.add('notification_container')
        document.querySelector('body').appendChild(container)
    }
    // message_sound.play()
    document.getElementById('new_message_sound').play();
    container.innerHTML += n_data.html
    setTimeout( () => {
        container.children[0].remove()
    }, 5000)
}


function close_msg_notif(e) {
    const notif = e.parentNode.parentNode
    notif.remove()
}