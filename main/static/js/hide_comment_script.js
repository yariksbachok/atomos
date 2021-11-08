function hide_post(e, id){
    const post = e.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
    post.remove();
    fetch(`${window.location.protocol}/addhidepost?post_id=${id}`);
}

function link_api(){
    document.querySelector('.no_show_button').click();
}

function delete_post(e, id){
    console.log('assssss')
    const post = e.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
    post.remove();
    fetch(`${window.location.protocol}/delPost?post_id=${id}`);
}

function complain(e, id){
    console.log('assssss')
    const post = e.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
    post.remove();
    fetch(`${window.location.protocol}/addComplain?post_id=${id}`);
    fetch(`${window.location.protocol}/addhidepost?post_id=${id}`);
}

function addImg(e){
  document.querySelector('#uploadImage').click();
}

function toggle_pin(id){
    const url = `${window.location.protocol}/pin?id=${id}`
    fetch(url).then( (data) => {
        console.log(data)
        if(window.location.pathname.includes('profile')){
            window.location.reload()
        }
    })
}


