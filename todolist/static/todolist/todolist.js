function getCookie(name) {
    // For csrf_token    
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};




async function createNew(){
    console.log("function: createNew")
    
    var todo = document.getElementById("new-todo").value
    if (todo.length==0) {return false}

    console.log(`adding new todo: ${todo}`)

    await fetch('/new_entry', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            todo:todo,
        })
    })



    
}




// Main listener / caller
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded")

})