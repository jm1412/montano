// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);

function showRegister() {
    console.log("function: showRegister")
    byId("login-form").style.display = "none";
    byId("register-form").style.display = "block";
    return false;
} 

function showLogin() {
    console.log("function: showLogin")
    byId("login-form").style.display = "block";
    byId("register-form").style.display = "none";
}

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {
    byId("show-register").onclick = function(){showRegister()};
    byId("show-login").onclick = function(){showLogin()};
})