
function genID(serverNum) {
    return(serverNum + "" + (new Date).getTime());
}

const massage_input = document.querySelector( ' .input_message input')
const message_container = document.querySelector( '.all_message_user')
message_container.scrollTo({
    top:message_container.scrollHeight,
    behavior:'auto'
})

function create_message(id){
    let message_text = massage_input.value;
    const c = document.querySelector('.message_between_users')
    const message_container = document.querySelector('.all_message_user')
    if(!message_text || !(/\S/.test(message_text))){
        massage_input.focus();
        return
    }
    message_text = message_text.replace(/@([^ ]*)/g, (str) => {
        return `<a href="${window.location.hostname}/profile/${str.slice(1)}">${str}</a>`
    })
    const avatar = get_avatar()
    const msg_id = genID(5)
    const message_pattern = `
        <div message_id="${msg_id}" class="message_user_nome">
        <img src="${avatar}">
            <p>${message_text}
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M20 10C20 15.5228 15.5228 20 10 20C4.47715 20 0 15.5228 0 10C0 4.47715 4.47715 0 10 0C15.5228 0 20 4.47715 20 10ZM18 10C18 14.4183 14.4183 18 10 18C5.58172 18 2 14.4183 2 10C2 5.58172 5.58172 2 10 2C12.3582 2 14.478 3.02032 15.9422 4.64358L9 11.5858L6.20711 8.79289C5.81658 8.40237 5.18342 8.40237 4.79289 8.79289C4.40237 9.18342 4.40237 9.81658 4.79289 10.2071L7.58579 13C8.36684 13.7811 9.63317 13.781 10.4142 13L17.1015 6.31276C17.6755 7.41616 18 8.67019 18 10Z" fill="#A3ACBA"/>
            </svg>
            </p>
        </div>
    `
     message_container.innerHTML += message_pattern
            message_container.scrollTo({
                top: message_container.scrollHeight,
                behavior: 'smooth'})
    chat_socket.send(JSON.stringify({
        'text': message_text,
        'to_user': id,
        'message_id': msg_id
    }))
    massage_input.value = ''
    function get_avatar() {
        const src = document.querySelector('.avatar_user').getAttribute('src')
        return src
    }
    // if(!(/\S/.test(message_text))){
    //     console.log('here')
    //     massage_input.focus();
    //     return
    // }
    // fetch_data(`${window.location.protocol}/new_message?user_id=${id}&text=${message_text}`).then(
    //     (data) => {
    //         console.log(data)
    //         massage_input.value = "";
    //         message_container.innerHTML += data
    //         message_container.scrollTo({
    //             top:message_container.scrollHeight,
    //             behavior:'smooth'
    //         })
    //     }
    // )
    // const new_message = document.createElement('div');
    // new_message.classList.add('message_user_nome')
    // const msg_pattern = `
    //     <img src="/main/static/img/svg/user_logo.svg">
    //     <p>${message_text}</p>
    // `
    // new_message.innerHTML = msg_pattern;
    // message_container.insertBefore(new_message, message_container.children[0]);

}


massage_input.addEventListener( 'keyup', (e) =>{
    if( e.key != 'Enter' && e.target.value ){
        return
    }
    const onclick_string = document.querySelector('.input_message button').attributes.onClick.value;
    const user_id_arr = onclick_string.split("(")[1].split("");
    user_id_arr.pop();
    const user_id = user_id_arr.join("");
    create_message(user_id);
})



async function fetch_data(url, options){
    const result = await fetch(url,{
        headers:{
            'Content-Type': 'application/json'
        }
    });
    return result.json();
}

const url = `ws://${window.location.host}/chat/${window.location.pathname.split('/')[2]}/`
console.log(url)
const chat_socket = new WebSocket(url)


chat_socket.onmessage =  (e) => {
    const data = JSON.parse(e.data).message
    console.log(data)
    if(data.type === 'read_message'){
        if(data.attempt){
            for( m_id of data.readed_messages){
                message_container.querySelector(`div[message_id="${m_id}"] svg`).remove()
            }
        }else{
            console.log('Server error')
        }
        // const message = document.querySelector(`div[message_id="${data.id}"]`)
        // message.getElementsByTagName('svg')[0].style.display = 'none'
    }else {
        const to_user_id = window.location.pathname.split('/')[2]
        if (data.to_user.id == to_user_id) {
            // message_container.innerHTML += data.from_user.msg
            // message_container.scrollTo({
            //     top: message_container.scrollHeight,
            //     behavior: 'smooth'
            // })
            if(data.user.is_readed){
                document.querySelector(`.message_user_nome[message_id="${data.to_user.msg.msg_id}"] svg`).remove()
            }
        } else if (data.to_user.id != to_user_id) {
            // message_container.innerHTML += data.to_user.msg
            // message_container.scrollTo({
            //     top: message_container.scrollHeight,
            //     behavior: 'smooth'
            // })
            const avatar = get_avatar()
            const message_pattern = `
                <div message_id="${data.to_user.msg.msg_id}" class="message_user">
                    <img src="${avatar}">
                    <p>${data.to_user.msg.text}</p>
                </div>
            `
            message_container.innerHTML += message_pattern
            message_container.scrollTo({
                top: message_container.scrollHeight,
                behavior: 'smooth'})
            }
        // message_container.innerHTML += data.message
        // message_container.scrollTo({
        //     top:message_container.scrollHeight,
        //     behavior:'smooth'
        // })
    }
    function get_avatar() {
        const src = document.querySelector('.avatar_to_user').getAttribute('src')
        return src
    }
}

chat_socket.onopen = function(e){
    console.log('send read')
    let unreadMessages = document.querySelectorAll('.message_user p svg')
    if(unreadMessages.length === 0){
        return
    }
    let unread_ids = []
    for(let i = 0; i < unreadMessages.length; i++) {
         unread_ids.push(unreadMessages[i].parentNode.parentNode.getAttribute('message_id'))
    }
    console.log(unread_ids)
    chat_socket.send(JSON.stringify({
        "type": "read_message",
        "messages_id": unread_ids
    }))
}