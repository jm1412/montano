// GLOBAL VARIABLES
// I use sitewide variables so I can load all products and work with those products, reducing server calls.
let products = "";
let orders = {};


// HELPER FUNCTIONS

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

function clearOrders(){
    // Clear orders object, consequently clears the modal and bottom bars.
    orders={};
    updateBottomBar()
}

function clearPos(){
    // Helper function
    // Clear main POS view
    posContainer = document.getElementById("pos-items-container")
    posContainer.innerHTML = ""
}

function clearConfirmationPage(){
    // Helper function
    // Clears confirmation modal page
    document.getElementById("payment").value = 0;
    document.getElementById("order-change").value = 0;
    document.getElementById("order-total").value = 0
}

function closeOrder(){
    // Helper function
    // Closes the order modal
    modal = document.getElementById("modal");
    modal.setAttribute("open",false)
}

function clearModal(){
    // Helper function
    container = document.getElementById("pos-orders");
    container.innerHTML = "";
}

// FUNCTIONS

async function getProducts(){
    // This gets run first via DOMContentLoaded
    // Get products and assigns them to global variable products for use sitewide.
    console.log("running")
    let r = await fetch('/get-products', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    })
    products = await r.json()
    console.log(products)
}

function pos_home(){
    // This gets loaded after the products are loaded.
    // Loaded via DOMContentLoaded.
    // Shows POS home screen.
    clearPos()
    createPosItem('/static/skc/images/pos-regular.jpg', "showProduct('regular')")
    createPosItem('/static/skc/images/pos-bento.jpg', "showProduct('bento)")
    createPosItem('/static/skc/images/pos-customized.jpg', "showProduct('regular', true)")
    createPosItem('/static/skc/images/pos-drinks.jpg', "showProduct('drinks')")
    createPosItem('/static/skc/images/pos-breads.jpg', "showProduct('bread-pastries')")
    createPosItem('/static/skc/images/pos-add.jpg', "showProduct('addons')")
}

function modalHandler(){
    // Runs after pos_home is shown.
    // Modal listener
    let modal = document.getElementById("modal");

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
        closeOrder()
        }
    }
}

function viewOrder(){
    // When view order button of bottom bar is pressed, show modal of order summary.
    
    clearModal()
    let orderEntry = "";
    Object.keys(orders).forEach(function(order){
        let quantity = orders[order].qty
        let price = orders[order].price
        item = products.find(item=> item.id == order)
        orderEntry += createOrderEntry(item, quantity, price)
    })

    container = document.getElementById("pos-orders")
    container.innerHTML += orderEntry

    // Show modal
    modal = document.getElementById("modal");
    modal.setAttribute("open", true);
}

async function posConfirm(){
    // On modal confirm, shows payment "page" inside same modal.
    // Do not submit to server yet.
    modal = document.getElementById("modal");
    modal.setAttribute("open",false)
    
    document.getElementById("payment").value = "";
    document.getElementById("order-change").value ="";
    let total = document.getElementById("pos-total").innerHTML
    document.getElementById("order-total").value = total


    confirmationPage = document.getElementById("confirmation-page")
    confirmationPage.setAttribute("open",true)
}

async function posSubmit(){
    // Submit orders to server.
    submitButton = document.getElementById("pos-confirm-button")
    submitButton.classList.add("disabled")

    let r = await fetch('/pos-submit', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            orders
        })
    })
    let response = await r.json()
    
    if (response.message == "success"){
        clearConfirmationPage()
        clearOrders()
        confirmationPage = document.getElementById("confirmation-page")
        confirmationPage.setAttribute("open",false)
    }

    submitButton.classList.remove("disabled")
}

function createOrderEntry(item, quantity, price){
    // Creates an "item" entry that can then be shown in vieworder modal.

    container = document.getElementById("modal-container")
    
    let total =  quantity * price
    orderItem = `
    <div class="modal-items-container">
        <div class="modal-items">
            <img class="order-image" src="${item.image}">
        </div>
        <div class="modal-items">
            ${item.name}
        </div>
        <div class="modal-items">
            ${price}
        </div>
        <div class="modal-items">
            <span onclick="changeQuantity('decrease', ${item.id});">
                <i class="fa-solid fa-chevron-left"></i>
            </span>
            
            <span id="${item.id}">${quantity}</span>
            <span onclick="changeQuantity('increase', ${item.id});">
                <i class="fa-solid fa-chevron-right"></i>
            </span>
        </div>
        <div  class="modal-items">
            ${total}
        </div>
    </div>
    `

    return orderItem;
    // container.innerHTML += orderItem;
}

function changeQuantity(direction, itemId){
    // Increases/decreases item quantity in orders.
    // Deletes item if quantity is 0.

    if (direction == "increase"){
        orders[itemId].qty ++
    } else {
        orders[itemId].qty --
    }

    if (orders[itemId].qty <= 0){
        delete orders[itemId]
    }

    viewOrder()
    updateBottomBar()
}

function updateBottomBar(){
    // Updates count and total in bottom bar.
    let total = 0
    let count = 0
    Object.keys(orders).forEach(function(order){
        let quantity = orders[order].qty
        let price = orders[order].price
        
        total += (price * quantity)
        count += (1 * quantity)

        // item = products.find(item => item.id == order)
    })
    
    // Display
    displayTotal = document.getElementById("bottom-bar-total")
    displayTotal.innerHTML = "Php " + total.toLocaleString()

    displayCount = document.getElementById("bottom-bar-count")
    if (count == 1){
        displayCount.innerHTML = count + " item"
    } else {
        displayCount.innerHTML = count + " items"
    }

    // Updates modal bottom bar too
    modalTotal = document.getElementById("pos-total")
    modalTotal.innerHTML = total
}

function addToOrder(itemId){
    // When item entry in POS is clicked, add target to order object.
    item = products.find(product => product.id === itemId);
    
    if (itemId in orders) {
        orders[itemId].qty ++;
    } else {
        orders[itemId] = {"qty":1, "price": item.price}
    }
    updateBottomBar()
}

function showProduct(category, customized=false){
    // Changes POS view to product view
    clearPos()
    Object.keys(products).forEach(function(product){
        var item = products[product];

        if(item.category == category && item.customized == customized){
            createPosItem(item.image, `addToOrder(${item.id})`)
        }
    })
}

function createPosItem(image, onClickFunction){
    // Creates "items" for POS home screen.
    // This function does not return anything but appends created item to pos home screen directly.

    posItem = document.createElement('div');
    posItem.classList.add("pos-items");
    posImage = document.createElement('img');
    posImage.src=image
    posImage.setAttribute("onclick",`${onClickFunction};`)
    posItem.appendChild(posImage);
    posContainer = document.getElementById("pos-items-container")
    posContainer.appendChild(posItem)
}

function calculateChange(){
    // Calculates change in pos confirmation modal, runs directly via onchange html tag
    let payment = document.getElementById("payment").value
    let total = document.getElementById("order-total").value
    let change = document.getElementById("order-change")

    change.value = payment - total
}

async function generateReport(){
    // Gets called from reports.html, value from html and submits to django for processing.
    fromDate = document.getElementById("reportFromDate")
    toDate = document.getElementById("reportToDate")
    reportType = document.querySelector('input[name="reportType"]:checked').value
    
    let r = await fetch('/generate_report', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            "from_date": fromDate,
            "to_date": toDate,
            "report_type": report_type
        })
    })
    let response = await r.json()
    
}

// Run these on load
document.addEventListener('DOMContentLoaded', async function() {
    modalHandler();
    getProducts(); // Load all products in memory
    pos_home();
})