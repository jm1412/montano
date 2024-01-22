// GLOBAL VARIABLES
// I use sitewide variables so I can load all products and work with those products, reducing server calls.

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

async function showTransactionHistory(){
    salesContainer = document.getElementById("sales-container");

    let r = await fetch('/get-transactions', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    })
    data = await r.json()
    sales = data.sales
    items = data.items

    Object.keys(sales).forEach(function(i){
        sale = sales[i]

    })
}

// Run these on load
document.addEventListener('DOMContentLoaded', async function() {
    showTransactionHistory();
})