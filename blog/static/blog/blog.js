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
        <div class="card mb-3 p-2">
            <div id="card-body">
            <a class="page-link" href="${blog.id}"><h5 class="card-title">${blog.title}</h5></a>
                <p class="card-text">${blog.body}</p>
            </div>
        </div>
        `

        element.innerHTML = html;

        document.getElementById("blogs").append(element);

    }) // blog.forEach
}

async function placePaginatorButtons(current_page = 1){
    
    let response = await number_of_pages(); 
    let max_pages = await response.json();
    
    if (max_pages > 1) {
        // First, figure out which buttons to create
        if (current_page == 1) {
            var page_numbers = [1, 2];

            if(max_pages > 2) {
                page_numbers.push(3);
            }

        } else { // current_page is not 1

            var page_numbers = [current_page-1, current_page];

            if (max_pages > current_page){
                page_numbers.push(current_page+1);
            }
        }

        // Then, create buttons
        var pagination_elements = []

        pagination_elements.push(`
            <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
        `);

        page_numbers.forEach(function(page_number){
            pagination_elements.push(`
                <li class="page-item"><a class="page-link" href="#" onClick="getBlogs(${page_number}); return false;">${page_number}</a></li>
                `)
        });

        pagination_elements.push(`
                <li class="page-item">
                    <a class="page-link" href="#" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
            </ul>
            </nav>
        `)

        // Render html
        var pagination_elements_html = pagination_elements.join('');

        var pagination_area = document.getElementById("pagination-buttons");
        pagination_area.innerHTML = pagination_elements_html

    }

}

async function number_of_pages(){
    // Returns maximum number of pages for paginator

    let pages = await fetch('number_of_pages', {
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin'
    }) // fetch

    return pages
}

async function updatePaginatorButtons(){
    // todo
}

function modalHandler(){
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