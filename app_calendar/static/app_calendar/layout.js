// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {

    // Update dropdown label
    console.log("Updating dropdown label")
    var currentView = window.location.pathname;
    var currentLabel = byId("navbardropdown-views")

    if (currentView=="/year"){
        currentLabel.innerHTML = "Year";
    } else if (currentView=="/month"){
        currentLabel.innerHTML = "Month";
    }
})