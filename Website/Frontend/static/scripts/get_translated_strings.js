var button = document.querySelector('#get_str_form_js')
if (button){
    button.addEventListener('click', (event)=>{
        var container = document.querySelector('#toast-messages')
        var el = document.createElement('div')
        el.classList.add('alert')
        el.classList.add('alert-success')
        var text_holder = document.createElement('span')
        text_holder.innerText = gettext("Это строчки из JS кода")
        el.insertAdjacentElement('afterbegin', text_holder)
        container.insertAdjacentElement('afterbegin', el)
    })
}