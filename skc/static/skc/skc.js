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

async function number_of_pages(){
    let pages = await fetch('number-of-pages',{
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin'
    })
}

async function placePaginatorButtons(current_page = 1){
    let response = await number_of_pages();
    let max_pages = await response.json();

    // Prepare which buttons to create.
    if (current_page == 1){
        var page_numbers = [1, 2];

        if (max_pages > 2){
            page_numbers.push(3);
        }
    } else {
        var page_numbers = [current_page-1, current_page];

        if (max_pages > current_page){
            page_numbers.push(current_page+1);
        }
    }

    // Create buttons
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

async function getCustomizedCakes(page, product_count = 0){
    // Get products and display them

    // Get products
    let response = await fetch(`get-customized-cakes/${page}`, {
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    })
    const products = await response.json();

    // Display products
    await products.forEach(function(product){
        console.log(`displaying ${product.image}`)
        product_count +=1
        target = document.getElementById(`customized-cake-image-${product_count}`)
        target.innerHTML = `<img class="catalog-photo" src='static${product.image}'>`

    })

}

// Main listener / caller
document.addEventListener('DOMContentLoaded', async function() {
    var currentView = window.location.pathname;
    console.log(`DOM Content Loaded, path: ${currentView}`)
    if (currentView=="/customized-cakes"){
        getCustomizedCakes(1)
    }
})