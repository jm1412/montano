// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);

function getCookie(name) {
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

function year_onclickday_save(todo, complete_by){
    console.log("year_on_clickday_save is running")
    console.log(`todo: ${todo}`)
    console.log(`complete_by: ${complete_by}`)
    // This is a helper function
    // that saves the value on textbox
    // I separated this to a smaller function because
    // I am adding various listeners to the main function


    // save
    // tic year_highlight

    fetch('/create_entry', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode:"same-origin",
        body: JSON.stringify({
            subject: todo,
            body:"",
            complete_by: complete_by,
            year_highlight: true
        })
    })
    console.log("saved")
    
}

function year_onclickday() {
    // When year view day entry is clicked, this function gets called
    // This function creates a textbox where user can enter new todo
    // Adds various listeners to text box:
        // on Enter
        // on out of focus
            //then calls save function
    target_date = this.id
    
    // Show text box
    this.innerHTML=`<input class="abcd" id="new-calendar-entry" type="text">`
    byId("new-calendar-entry").focus()

    // Add listeners to text box
    var input = document.getElementById("new-calendar-entry");

    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent default action
            byId("new-calendar-entry").blur()
        }
    })

    input.addEventListener("focusout", function(){
        this.outerHTML = this.value;
        year_onclickday_save(this.value, target_date);
    }); 
};


function generateYearPlaceholder(){
    const months = {
        january:"31",
        february:"29",
        march:"31",
        april:"30",
        may:"31",
        june:"30",
        july:"31",
        august:"31",
        september:"30",
        october:"31",
        november:"30",
        december:"31"
    };

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
        target.innerHTML = `<div class="yv-m-label">${key}</div>`;
        
        target_days = Number(months[key])+1
        for (let i = 1; i<target_days; i++) {

            var dd = i.toLocaleString('en-US', {minimumIntegerDigits: 2,useGrouping: false}) // trailing 0
            
            target.innerHTML+=`
            <div class="yv-d-container d-flex">
            <div class="yv-d">${i}</div>
            <div class="yv-todo flex-grow-1" id="${key} ${dd} 2023"></div>
            </div>`
        }
    }

    // listener to edit/add calendar entries on click
    var elements = document.getElementsByClassName("yv-todo");

    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', year_onclickday, false);
    }
}

// fetch year todo and insert received json file to corresponding html id
function getCalendarYear() { 
    console.log("getCalendarYear is running")
    fetch('./get_calendar_year')
    .then(response => response.json())
    .then(calendar => {
        calendar.forEach(function(item) {
            console.log(item.complete_by.toLowerCase());
            byId(item.complete_by.toLowerCase()).innerHTML = item.todo

        })
    })
}

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {

    // Update dropdown label
    console.log("Updating dropdown label")
    var currentView = window.location.pathname;
    var currentLabel = byId("navbardropdown-views")

    // Run necessary scripts per view type
    if (currentView=="/year"){
        currentLabel.innerHTML = "Year";
        generateYearPlaceholder()
        getCalendarYear()
    } else if (currentView=="/month"){
        currentLabel.innerHTML = "Month";
    }
})