// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);


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
}

function year_onclickday() {
    // When year view day entry is clicked, this function gets called
    // This function creates a textbox where user can enter new todo
    // Adds various listeners to text box:
        // on Enter
        // on out of focus
            //then PUTS
    console.log(`year_onclickday : ${this.innerHTML}`)
    target_date = this.id

    if (this.innerHTML.length > 0) {
        var write_type = "edit";
    } else {
        var write_type = "new";
    }

    console.log(`write_tye = ${write_type}`)
    
    // Show text box
    this.innerHTML=`<input id="new-calendar-entry" style="text-align:left" type="text" onclick="event.stopPropagation()" value="${this.innerHTML}">`
    byId("new-calendar-entry").focus()

    // Add listeners to text box
    var input = document.getElementById("new-calendar-entry");

    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent default action
            byId("new-calendar-entry").blur() // to trigget focus out
        }
    })

    input.addEventListener("focusout", function(){
        this.outerHTML = this.value;

        fetch('/create_entry', {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode:"same-origin",
            body: JSON.stringify({
                subject: this.value,
                body:"",
                complete_by: target_date,
                year_highlight: true,
                write_type:write_type
            })
        })
        console.log("saved")
    }); 
};


function generateYearPlaceholder(){
    const months = {
        1:"31",
        2:"29",
        3:"31",
        4:"30",
        5:"31",
        6:"30",
        7:"31",
        8:"31",
        9:"30",
        10:"31",
        11:"30",
        12:"31"
    };

    const monthNames = {
        1:"january",
        2:"february",
        3:"march",
        4:"april",
        5:"may",
        6:"june",
        7:"july",
        8:"august",
        9:"september",
        10:"october",
        11:"november",
        12:"december"
    }

    // Generate calendar placeholders
    for (var key in months){

        // Generate container
        monthContainer = byId("months-container")
        monthContainer.innerHTML += `
        <div id="container-${key}" class="p-1 yv-m flex-shrink-0">
        </div>
        `

        // Generate month label and placeholder days
        var targetId = "container-" + key;
        var target = byId(targetId);
        target.innerHTML = `<div class="yv-m-label">${monthNames[key]}</div>`;
        
        target_days = Number(months[key])+1
        for (let i = 1; i<target_days; i++) {

            var dd = i.toLocaleString('en-US', {minimumIntegerDigits: 2,useGrouping: false}) // trailing 0
            var mm = Number(key).toLocaleString('en-US', {minimumIntegerDigits: 2,useGrouping: false})

            target.innerHTML+=`
            <div class="yv-d-container d-flex">
            <div class="yv-d">${i}</div>
            <div class="yv-todo flex-grow-1" id="2023-${mm}-${dd}"></div>
            </div>`
        }
    }

    // listener to edit/add calendar entries on click
    var elements = document.getElementsByClassName("yv-todo");

    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', year_onclickday, false);
    }
}


function getCalendarYear() { 
    // Populate todo list

    console.log("getCalendarYear is running")
    fetch('./get_calendar_year')
    .then(response => response.json())
    .then(calendar => {
        calendar.forEach(function(item) {
            console.log(`item.complete_by: ${item.complete_by}`);
            byId(item.complete_by).innerHTML = item.todo
        })
    })
}

function highlight_today(){
    // Highlight today's color
    var today = new Date();
    today = today.toISOString().slice(0, -14);
    byId(today).parentNode.style.backgroundColor = "lightskyblue";
}

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {

    // Update dropdown label
    console.log("Updating dropdown label")
    var currentView = window.location.pathname;
    // var currentLabel = byId("navbardropdown-views")

    // Run necessary scripts per view type
    if (currentView=="/year"){
        // currentLabel.innerHTML = "Year";
        generateYearPlaceholder()
        getCalendarYear()
    } else if (currentView=="/month"){
        currentLabel.innerHTML = "Month";
    }

    // Set today's color
    highlight_today()
})