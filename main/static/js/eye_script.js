function eye_toggler_lr(e){
    psw_input = e.parentNode.parentNode.parentNode.querySelector(".form_email")
    psw_input.attributes.type.nodeValue = psw_input.attributes.type.nodeValue ? "" : "password"
    e.attributes.src.nodeValue = e.attributes.src.nodeValue === "/main/static/img/svg/eye_none.svg" ?
                                        "/main/static/img/svg/show.svg" : "/main/static/img/svg/eye_none.svg"
    console.log(psw_input.attributes)
}

