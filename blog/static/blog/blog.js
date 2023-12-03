function getCookie(name) {
    // Cookie handler for csrf token

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

async function getBlogs(page){
    // Get blogs and display them
    
    // Get blogs
    let response = await fetch(`get_blogs/${page}`, {
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    }) // fetch
    const blogs = await response.json();

    // Display blogs    
    document.getElementById("blogs").innerHTML=""
    blogs.forEach(function(blog) {
        // Generate blog posts here
        let element = document.createElement('div');
        element.className = "blog_entry";
        element.id = blog.id;
    
        html = `
        <article>
            <a href="${blog.id}">
                <p class="blog-title">${blog.title}</p>
            </a>
            <p class="blog-body">${blog.body.slice(0,100).trim()}</p>
        </article>
        `

        element.innerHTML = html;

        document.getElementById("blogs").append(element);

    }) // blog.forEach
}

async function updatePaginatorButtons(){
    // todo
}

function modalHandler(){ // DEPRACATED
    // Handles modal functions.

    // MODAL COMPOSE
    // Get the modal
    var modal = document.getElementById("blog");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("btn-close")[0];


    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    }
}

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {
    var currentView = window.location.pathname;
    if (currentView=="/blog/"){
        getBlogs(1) // On load generate first page of blog
        placePaginatorButtons()
    }

    modalHandler()
})