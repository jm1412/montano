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

function showCake(image){
    modal = document.getElementById("modal");
    var modalImage = document.getElementById("modal-image");
    console.log(image)
    image = `<img src='${image}'>`
    console.log(image)
    modalImage.innerHTML = image
    modal.setAttribute("open", true);
}

function hideCake(){
    modal = document.getElementById("modal");
    modal.setAttribute("open", false);
}

function modalHandler(){
    // Modal listener

    let modal = document.getElementById("modal");

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
        hideCake()
        }
    }
}

// Main listener / caller
document.addEventListener('DOMContentLoaded', async function() {
    modalHandler()
})