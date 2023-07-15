// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);

// Global variables
var currentYear = "";
var currentMonth = "";
    // these will have to be added inside functions soon

const months = {
    1:"31",2:"29",3:"31",4:"30",5:"31",6:"30",7:"31",8:"31",9:"30",10:"31",11:"30",12:"31"
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
};

const monthColors = {
    1: "#F8D7DA",    // Pale Rose
    2: "#FCE4EC",    // Lavender Blush
    3: "#F1EEF6",    // Lilac
    4: "#DDEBF7",    // Baby Blue
    5: "#E9F7EF",    // Mint Cream
    6: "#F8F8E7",    // Vanilla
    7: "#FCE8D5",    // Peachy Beige
    8: "#F3F3F3",    // Pale Gray
    9: "#F7ECE1",    // Ivory
    10: "#F3F8F2",   // Pale Green
    11: "#EAE7F2",   // Lilac Gray
    12: "#F2E9E4"    // Soft Peach
};

function getCookie(name) {
    // For csrf_token
    console.log("getCookie")
    
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
    previous_val = this.innerHTML

    this.innerHTML=`<input id="new-calendar-entry" style="text-align:left" type="text" onclick="event.stopPropagation()" value="${this.innerHTML}">`
    byId("new-calendar-entry").focus()

    // Add listeners to text box
    var input = document.getElementById("new-calendar-entry");

    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent default action
            byId("new-calendar-entry").blur() // to trigget focus out
        } else if (event.key === "Ecape"){
            console.log("escape is pressed")
        }
    })

    input.addEventListener("focusout", function(){
        this.outerHTML = this.value;

        fetch('/create_entry', {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode:"same-origin",
            body: JSON.stringify({
                todo: this.value,
                detail:"",
                complete_by: currentYear +"-"+target_date,
                year_highlight: true,
                write_type:write_type
            })
        })
        console.log("saved")
    }); 
};


function generateYearPlaceholder(currentYear){
    // Generate calendar placeholders
    console.log("generateYearPlaceholder")

    for (var key in months){

        // Generate container
        monthContainer = byId("months-container")
        monthContainer.innerHTML += `
        <div id="container-${key}" class="p-1 yv-m flex-shrink-0" style="background-color:${monthColors[key]}">
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
            <div class="yv-todo flex-grow-1 todo-container" id="${mm}-${dd}"></div>
            </div>`
        }
    }

    // listener to edit/add calendar entries on click
    var elements = document.getElementsByClassName("yv-todo");

    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', year_onclickday, false);
    }
}


function getCalendarYear(currentYear) { 
    // Populates to do list

    // Clear todo list
    console.log("getCalendarYear")

    var elements = byClass("todo-container")
    for (var i = 0; i < elements.length; i++) {
        elements[i].innerHTML = "";
    }

    // Populate todo list
    console.log("getCalendarYear is running")
    fetch('./get_calendar_year/'+currentYear)
    .then(response => response.json())
    .then(calendar => {
        calendar.forEach(function(item) {
            console.log(`item.complete_by: ${item.complete_by.slice(5,)}`);
            byId(item.complete_by.slice(5,)).innerHTML = item.todo
        })
    })
}

function highlight_today(){
    // Highlight today's color
    console.log("highlight_today")

    var today = new Date();
    today_y = today.toISOString().slice(0,4)
    today = today.toISOString().slice(5, -14);

    byId(today).parentNode.style.backgroundColor = ""; // Remove colors first, in case of year change

    if (currentYear == today_y){
        byId(today).parentNode.style.backgroundColor = "#A491D3";
    }
}

function yearChanger_y() {
    // When year changer button is clicked,
    // update new year
    // query new year
    console.log("yearChanger_y")

    byId("prev-year").addEventListener("click", function(){
        this.disabled=true;

        byId("current-year").innerHTML = Number(byId("current-year").innerHTML)-1
        currentYear = byId("current-year").innerHTML
        getCalendarYear(currentYear)
        highlight_today()
        this.disabled=false;
    })

    byId("next-year").addEventListener("click", function(){
        this.disabled=true;

        byId("current-year").innerHTML = Number(byId("current-year").innerHTML)+1
        currentYear = byId("current-year").innerHTML
        getCalendarYear(currentYear)
        highlight_today()

        this.disabled=false;
    })
}

function yearChanger_m() {

    byId("prev-year").addEventListener("click", function(){
        this.disabled=true;
        byId("current-year").innerHTML = Number(byId("current-year").innerHTML)-1
        currentYear = byId("current-year").innerHTML
        generateMonthPlaceholder()
        getCalendarMonth(currentYear, currentMonth)
        this.disabled=false;

    })

    byId("next-year").addEventListener("click", function(){
        this.disabled=true;
        byId("current-year").innerHTML = Number(byId("current-year").innerHTML)+1
        currentYear = byId("current-year").innerHTML
        generateMonthPlaceholder()
        getCalendarMonth(currentYear, currentMonth)
        this.disabled=false;
    })
}

function monthChanger_m() {
    // Similar to year changer but changes month instead

    byId("prev-month").addEventListener("click", function(){
        this.disabled=true;
        if (currentMonth > 1) {
            byId("current-month").innerHTML = Number(byId("current-month").innerHTML)-1
        } else {
            byId("current-month").innerHTML = 12;
            byId("current-year").innerHTML = Number(byId("current-year").innerHTML)-1
            currentYear = byId("current-year").innerHTML
        }
        currentMonth = byId("current-month").innerHTML

        generateMonthPlaceholder()
        getCalendarMonth(currentYear, currentMonth)

        this.disabled=false;
    })

    byId("next-month").addEventListener("click", function(){
        this.disabled=true;
        
        if (currentMonth <12) {
            byId("current-month").innerHTML = Number(byId("current-month").innerHTML)+1
        } else {
            byId("current-month").innerHTML = 1;
            byId("current-year").innerHTML = Number(byId("current-year").innerHTML)+1
            currentYear = byId("current-year").innerHTML    
        }
        currentMonth = byId("current-month").innerHTML
        
        generateMonthPlaceholder()
        getCalendarMonth(currentYear, currentMonth)
        
        this.disabled=false;
    })
}

function getCalendarMonth(currentYear, currentMonth) {
    // Generate day labels
    // Populate monthly todo
    
    // // Clear day label
    // var clean = byClass("month-day-label")
    // for (var i=0; i < clean.length; i++) {
    //     clean[i].innerHTML = "";
    // }
    
    // for some reason this isn't needed anymore wtf?

    // Clear todo list
    var elements = byClass("month-todo-container")
    for (var i = 0; i < elements.length; i++) {
        elements[i].innerHTML = "";
    }



    

    // Calendar color
    byId("calendar-month-container").style.backgroundColor = monthColors[currentMonth];

    // Month name
    byId("current-month-name").innerHTML = monthNames[currentMonth];

    // For day of the week offset
    var firstDay = new Date(Number(currentYear), Number(currentMonth)-1, 1);

    // Generate labels
    // Day label
    target_days = Number(months[currentMonth])+1    
    for (let i = 1; i<target_days; i++) {
        targetElement = byId(`label-${Number(i) + Number(firstDay.getDay())}`).innerHTML = i
    }

    // Get data and add to calendar
    var mm = currentMonth.toLocaleString('en-US', {minimumIntegerDigits: 2,useGrouping: false})
    yearMonth = currentYear + mm
    fetch('./get_calendar_month/'+yearMonth)
    .then(response => response.json())
    .then(calendar => {
        calendar.forEach(function(item) {
            let element = document.createElement('div');
            element.className = 'todo-entry';
            element.id = item.id;
            element.innerHTML = item.todo;


            element.addEventListener('click', function(e) {
                e.stopPropagation()
                console.log(`${item.todo} is clicked with completeby: ${item.complete_by} and time: ${item.complete_time}`);
                modalHandler(item,"update");
            })

            byId(`day-${Number(item.complete_by.slice(8,11))+firstDay.getDay()}`).append(element);
            
        })
    })

    // highlight today
    highlight_month(currentYear, currentMonth)

}

function modalHandler(item, wt, newDate) {   
    // Populate modal
    byId("modal-complete-by").value = item.complete_by || newDate || "";
    byId("modal-complete-time").value = item.complete_time || "";
    byId("modal-todo").value = item.todo || "";
    byId("modal-detail").value = item.detail || "";
    write_type = wt;

    var modal = document.getElementById("myModal");
    
    modal.style.display = "block";

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    
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

    // When modal is submitted
    document.querySelector('#save-calendar').addEventListener('click', function() {
        console.log("MODAL creating new item")
        modal.style.display = "none";
        
        var loading = true;

        if (loading){
            fetch('/create_entry', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                mode:"same-origin",
                body: JSON.stringify({
                    id: item.id,
                    todo: byId("modal-todo").value,
                    detail:byId("modal-detail").value,
                    complete_by: byId("modal-complete-by").value,
                    complete_time: byId("modal-complete-time").value,
                    year_highlight: false,
                    write_type:write_type
                })
            })
        }

        byId("modal-complete-by").value = "";
        byId("modal-complete-time").value = "";
        byId("modal-todo").value = "";
        byId("modal-detail").value = "";

        getCalendarMonth(currentYear, currentMonth)

        loading = false;
    });

    // Delete entry
    document.querySelector('#month-delete-todo').addEventListener('click', function() {
        console.log("MODAL deleting item")
        modal.style.display = "none";

        console.log(`deleting entry: ${item.id}`)

        var loading = true;

        if (loading) {
            fetch('/create_entry', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                mode:"same-origin",
                body: JSON.stringify({
                    id:item.id,
                    write_type:"delete"
                })
            })
        }

        byId("modal-complete-by").value = "";
        byId("modal-complete-time").value = "";
        byId("modal-todo").value = "";
        byId("modal-detail").value = "";

        getCalendarMonth(currentYear, currentMonth)

        loading = false;
    })
}

function generateMonthPlaceholder() {
    // Generate calendar placeholders for month view
    // currentYear -> int
    // currentMonth -> int
    //  currently getting currentYear and currentMonth from global var of their innerhtml

    // Generate placeholder divs
    var monthContainer = byId("calendar-month-container");
    monthContainer.innerHTML=""; // clear
    
    monthContainer.innerHTML += `
        <div class="row">
            <div class="col calendar-month" id="mv-month-name"></div>
        </div>
        `;

    var targetRow = "";

    for (let i=0; i<6; i++) { // rows
        monthContainer.innerHTML += `
            <div class="row calendar-month-days-row" id="month-row-${i}">
            </div>
        `;
        
        var firstDay = new Date(Number(currentYear), Number(currentMonth)-1, 1);
        targetRow = byId(`month-row-${i}`);
        for (let j=1; j<8; j++) { // days per row
            targetRow.innerHTML+=`
                <div class="col calendar-month-days-box" id="${currentYear}-${currentMonth}-${j+(7*i)-firstDay.getDay()}">
                    <div class="month-day-label" id="label-${j+(7*i)}"></div>
                    
                    <div class="month-todo-container" id="day-${j+(7*i)}">

                    </div>
                </div>
            `;
        }
    }

    // Create new entry
    var boxes = byClass("calendar-month-days-box");
    for (var i = 0; i < months[currentMonth]; i++) {
        boxes[i+firstDay.getDay()].addEventListener('click', function(e){
            e.stopPropagation();
            modalHandler("","new",this.id);
        })
    }
}

function highlight_month(currentYear, currentMonth) {
    // Highlight current day of the month on month view

    var today = new Date();
    today_y = today.toISOString().slice(0,4);
    today_m = Number(today.toISOString().slice(5,7));
    today_d = today.toISOString().slice(8,-14); // could cause potential issue on single digit days, needs to be observed
    today = `${today_y}-${today_m}-${today_d}`
    console.log(`coloring today: ${today}`)

    try {
        byId(today).querySelector(".month-day-label").style.backgroundColor = "lightskyblue";
    }
    catch(err) {
        console.log("nothing to color");
    }


}


// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded")

    // Update dropdown label
    console.log("Updating dropdown label")
    var currentView = window.location.pathname;
    // var currentLabel = byId("navbardropdown-views")

    // Run necessary scripts per view type
    if (currentView=="/year"){
        // currentLabel.innerHTML = "Year";
        currentYear = byId("current-year").innerHTML
        generateYearPlaceholder()
        getCalendarYear(currentYear)
        yearChanger_y()
        // Set today's color
        highlight_today()
    } else if (currentView=="/month"){
        currentYear = byId("current-year").innerHTML
        currentMonth = byId("current-month").innerHTML

        generateMonthPlaceholder()
        yearChanger_m()
        monthChanger_m(currentMonth)
        getCalendarMonth(currentYear, currentMonth)
        highlight_month(currentYear, currentMonth)
    }
})



// FOR FUNSIES
function parseDateToISOString(userInput) {
    // Remove any leading/trailing white spaces
    userInput = userInput.trim();
  
    // Define the months in different formats
    const months = [
      { name: 'January', short: 'jan', number: '01' },
      { name: 'February', short: 'feb', number: '02' },
      { name: 'March', short: 'mar', number: '03' },
      { name: 'April', short: 'apr', number: '04' },
      { name: 'May', short: 'may', number: '05' },
      { name: 'June', short: 'jun', number: '06' },
      { name: 'July', short: 'jul', number: '07' },
      { name: 'August', short: 'aug', number: '08' },
      { name: 'September', short: 'sep', number: '09' },
      { name: 'October', short: 'oct', number: '10' },
      { name: 'November', short: 'nov', number: '11' },
      { name: 'December', short: 'dec', number: '12' }
    ];
  
    // Check if the input matches any known format
    const matchISOFormat = /^(\d{4})-(\d{2})-(\d{2})$/;
    const matchMonthFormat = /^(\d{1,2})\s(\w{3})\s(\d{4})$/;
    const matchYMDFormat = /^(\d{4})(\d{2})(\d{2})$/;
    const matchSlashFormat = /^(\d{4})\/(\d{2})\/(\d{2})$/;
    const matchMMMDDYYYYFormat = /^(\w{3})\s(\d{1,2})[,]\s(\d{4})$/;
    const matchDDMMMYYYYFormat = /^(\d{1,2})\s(\w{3})\s(\d{4})$/;
    const matchDDMMYYYYFormat = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
    const matchYYYYMMDDFormat = /^(\d{4})\/(\d{1,2})\/(\d{1,2})$/;
    const matchYYYYMMMFormat = /^(\d{4})\s(\w{3})$/;
    const matchYYYYFormat = /^(\d{4})$/;
  
    // Try to match ISO format (YYYY-MM-DD)
    let match = userInput.match(matchISOFormat);
    if (match) {
      const year = match[1];
      const month = match[2];4
      const day = match[3];
      return new Date(year, month - 1, day).toISOString();
    }
  
    // Try to match Month format (DD MMM YYYY)
    match = userInput.match(matchMonthFormat);
    if (match) {
      const day = match[1];
      const monthStr = match[2].toLowerCase();
      const year = match[3];
  
      // Find the corresponding month based on the short or long name
      const month = months.find(
        m => m.name.toLowerCase().startsWith(monthStr) || m.short === monthStr
      );
  
      if (month) {
        return new Date(year, month.number - 1, day).toISOString();
      }
    }
  
    // Try to match YYYYMMDD format
    match = userInput.match(matchYMDFormat);
    if (match) {
      const year = match[1];
      const month = match[2];
      const day = match[3];
      return new Date(year, month - 1, day).toISOString();
    }
  
    // Try to match YYYY/MM/DD format
    match = userInput.match(matchSlashFormat);
    if (match) {
      const year = match[1];
      const month = match[2];
      const day = match[3];
      return new Date(year, month - 1, day).toISOString();
    }
  
  // Try to match MMM DD, YYYY format
  match = userInput.match(matchMMMDDYYYYFormat);
  if (match) {
    const monthStr = match[1].toLowerCase();
    const day = match[2];
    const year = match[3];

    // Find the corresponding month based on the short or long name
    const month = months.find(
      m => m.name.toLowerCase().startsWith(monthStr) || m.short === monthStr
    );

    if (month) {
      return new Date(year, month.number - 1, day).toISOString();
    }
  }

  // Try to match DD MMM YYYY format
  match = userInput.match(matchDDMMMYYYYFormat);
  if (match) {
    const day = match[1];
    const monthStr = match[2].toLowerCase();
    const year = match[3];

    // Find the corresponding month based on the short or long name
    const month = months.find(
      m => m.name.toLowerCase().startsWith(monthStr) || m.short === monthStr
    );

    if (month) {
      return new Date(year, month.number - 1, day).toISOString();
    }
  }

  // Try to match DD/MM/YYYY format
  match = userInput.match(matchDDMMYYYYFormat);
  if (match) {
    const day = match[1];
    const month = match[2];
    const year = match[3];
    return new Date(year, month - 1, day).toISOString();
  }

  // Try to match YYYY/MM/DD format
  match = userInput.match(matchYYYYMMDDFormat);
  if (match) {
    const year = match[1];
    const month = match[2];
    const day = match[3];
    return new Date(year, month - 1, day).toISOString();
  }

  // Try to match YYYY MMM format
  match = userInput.match(matchYYYYMMMFormat);
  if (match) {
    const year = match[1];
    const monthStr = match[2].toLowerCase();

    // Find the corresponding month based on the short or long name
    const month = months.find(
      m => m.name.toLowerCase().startsWith(monthStr) || m.short === monthStr
    );

    if (month) {
      return new Date(year, month.number - 1).toISOString();
    }
  }

  // Try to match YYYY format
  match = userInput.match(matchYYYYFormat);
  if (match) {
    const year = match[1];
    return new Date(year, 0).toISOString();
  }

  // If no match is found, return null or throw an error, depending on your use case
  return null;
}

// Usage example:
const userInput = 'jan 5, 2023';
const isoString = parseDateToISOString(userInput);
console.log(isoString);
