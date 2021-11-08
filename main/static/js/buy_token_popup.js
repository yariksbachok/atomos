//  обработчик событий для всплытия попапа

let user = '';
const btn_buy = document.querySelectorAll(".buy_token");
function show(){
    const popup = document.querySelector(".mng_panel_popup_buy_container.mpp");
    popup.classList.remove("no_show")
    popup.classList.add("show")
}
let BTC = 0
fetch('https://api.bitaps.com/market/v1/ticker/btcusd').then((response) => {
        return response.json();
      }).then((data) => {
        BTC = data['data']['last'];
      });

//  обработчик событий для скрытия попапа(бэкграунд)
const popup_container_buy = document.querySelectorAll(".mng_panel_popup_buy_container");
for( p of popup_container_buy){
    p.addEventListener('click', (e) => {
        if(e.target.classList.contains("mng_panel_popup_buy_container")){
            e.target.classList.remove('show');
            e.target.classList.add('no_show'); 
        }

    })
}
//  обработчик событий для скрытия попапа(крестик)
const cancel_popup_btn_buy = document.getElementsByClassName('blue_chrest')
for( let i = 0; i <cancel_popup_btn_buy.length; i++ ){
        
        cancel_popup_btn_buy[i].addEventListener('click', (e) => {
        const popup = cancel_popup_btn_buy[i].parentNode.parentNode.parentNode.parentNode;
        popup.classList.remove('show');
        popup.classList.add('no_show');
      
    })
}


function fill_popup_buy(event, id) {
    const url = `${window.location.protocol}/buy_popup?id=${id}`
    const popup_container = document.querySelector('.mng_panel_popup_buy_container.mpp')
    const preloader = popup_container.querySelector('.preloader')
    preloader.classList.add('show')
    preloader.classList.remove('no_show')
    // const preloader
    fetch_data(url).then(
        (data) => {
            preloader.classList.remove('show')
            preloader.classList.add('no_show')
            fill(popup_container, data)
        }
    )
}

async function fetch_data(url, options){
    const result = await fetch(url);
    return result.json();
}

function fill_popup_top_up(event, id) {
    const url = `${window.location.protocol}/buy_popup?id=${id}`
    const popup_container = document.querySelector('.mng_panel_popup_buy_container.tp_up')
    const preloader = popup_container.querySelector('.preloader')
    preloader.classList.add('show')
    preloader.classList.remove('no_show')
    // const preloader
    fetch_data(url).then(
        (data) => {
            preloader.classList.remove('show')
            preloader.classList.add('no_show')
            fill_top_up(popup_container, data)
        }
    )
}

function fill_top_up(popup, profile) {
    const token_cost_field = popup.querySelector('#token_cost')
    token_cost_field.innerText = `${profile.token_cost}`
}



function fill(popup, profile) {
    user = profile
    popup.querySelector('#user').innerText = `${profile.user.username}`
    popup.querySelector('#token_cost').innerText = `${profile.token_cost}`
    popup.querySelector('#token_procent').innerText = `${profile.procent}`
}



function buy_token(e){
    let you_give = e.value / BTC
    document.getElementById('you_give').value = you_give.toFixed(10)+' ₿'
    let give = e.value / user.token_cost
    document.getElementById('give').value = give.toFixed(10)+' токенов'

}



