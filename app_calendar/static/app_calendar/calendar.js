// Bindings
const query = document.querySelector.bind(document);
const queryAll = document.querySelectorAll.bind(document);
const byId = document.getElementById.bind(document);
const byClass = document.getElementsByClassName.bind(document);
const byTag = document.getElementsByTagName.bind(document);

function createEntry() {
    fetch('/create_entry', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
          read: false
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        // result.error checking here
    });
  }

// Main listener/caller
document.addEventListener('DOMContentLoaded', function() {
    byId("show-register").onclick = function(){createEntry()};
})