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

let page = 1;
let itemNumber = 0;
let currentPage = 0;
function loadImages(type) {
    const xhr = new XMLHttpRequest();
    currentPage += 1

    xhr.open('GET', `/get-images/${type}?page=${page}`, true);
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 400) {
            page += 1;

            const data = JSON.parse(xhr.responseText);

            console.log(`data.max_pages:${data.max_pages}`)
            if (data.max_pages < currentPage){
                return false;
            }
            for (let product of data.products) {
                itemNumber+=1;
                const img = document.createElement('img');
                img.classList.add("cake-page-image")
                img.id = itemNumber;
                img.src = product.image;
                img.onclick = function(){
                    // showCake(product.image, img.id)
                    getNextModal(0, type, img.id)
                };
                document.getElementById('image-container').appendChild(img);
            }

            // Check if more images need to be loaded immediately after the initial load
            if (window.innerHeight >= document.documentElement.scrollHeight) {
                if(page<=data.max_pages+1){
                    loadImages(type);
                }
            }
        } else {
            console.error('Error loading images.');
        }
    };

    xhr.onerror = function () {
        console.error('Error loading images.');
    };

    xhr.send();
}

async function getNextModal(direction=0, type, currentItemOverride=false){

    currentItem = currentItemOverride || document.getElementsByClassName("modal-image")[0].id;
    
    page = Number(currentItem) + Number(direction);
    let r = await fetch(`/get-one-image/${type}?page=${page}`, {
        method:'GET'
    })
    const response = await r.json();

    // Change details of modal
    itemName = document.getElementById("modal-item-name")
    itemPrice = document.getElementById("modal-item-price")

    itemName.innerHTML = response.products[0].name;
    
    if (response.products[0].price > 0){
        itemPrice.innerHTML = "Php " +response.products[0].price;
    } else{
        itemPrice.innerHTML="";
    }

    // To prevent overflow
    if (response.products[0].image == undefined){        
        page -= Number(direction)
    } else {
        showCake(response.products[0].image,page)
    }

    // Hide/show next/previous buttons
    nextButton = document.getElementById("modal-next-button")
    previousButton = document.getElementById("modal-previous-button")
    if(response.has_next){
        nextButton.style.visibility = "visible"
    } else{
        nextButton.style.visibility = "hidden"
    }

    if(response.has_previous){
        previousButton.style.visibility = "visible"
    }else{
        previousButton.style.visibility = "hidden"
    }


}

function showCake(image, id=0){
    modal = document.getElementById("modal");
    var modalImage = document.getElementById("modal-image-container");
    image = `<img id=${id} class="modal-image" src='${image}'>`
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
    // Initial load
    loadImages(type);

    // Infinite scroll
    window.addEventListener('scroll', function () {
        if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 100) {
            loadImages(type);
        }
    });
})