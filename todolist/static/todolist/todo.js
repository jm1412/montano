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

async function newTodo(){
    // Called from html, creates/adds new to do item entry.
    
    var todo = document.getElementById("new-todo").value
    if (todo.length==0) {return false};

    let r = await fetch('new_entry/', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            todo:todo
        })
    })
    const response = await r.json();

    document.getElementById("new-todo").value = "";

    // insert new todo item at index 0 and update everything
    let newTodo = createTodoElement(todo, response.todoId)
    let todoList = document.getElementById("todo-items");
    todoList.insertBefore(newTodo, todoList.children[0]);

    updateTaskOrder(todoList);
}

function createTodoElement(text, todoId, status=false) {
    // Helper function
    // Creates new todo element, returns created element.

    // todoId returns int id from models.py
    // onclick is added to span and ellipsis, but ellipsis has stop propagation

    let todoItem = document.createElement('li');
    todoItem.id = todoId
    todoItem.classList.add("item-entry");
    todoItem.classList.add("list-unstyled");
    todoItem.innerHTML = `
        <span onClick="editButton('${todoId}');" id="edit-button" class="popup">
            <span class="popuptext" id="popup-${todoId}">
                <ul class="edit-button-options" onClick="editThis(${todoId});">Edit</ul>
                <ul class="edit-button-options" onClick="deleteThis(${todoId});">Delete</ul>    
            </span>
            <i onClick="editButton('${todoId}'); event.stopPropagation();"class="fa-solid fa-ellipsis"></i>
        </span>

        <span id="checkbox-span">   
            <input class="form-check-input" type="checkbox" value="" id="${todoId}" ${status ? 'checked' : ''}>
        </span>

        <span id="label-span">
            <label class="form-check-label" for="${todoId}" id=text-entry-${todoId}>
            ${text}
            </label>
        </span>
    `
    todoItem.draggable = true;
    return todoItem
}

async function showTodoAsList(status=false, reset=false){
    // Displays todo as list in html.
    // List is ordered by position.
    
    let todoContainer = "";

    let todoItems = await getTodo(status);
    todoItems.forEach(function(todoItem){
        let element = createTodoElement(todoItem.title, todoItem.id, todoItem.status)
        todoContainer += element.outerHTML
    })

    // I created a container div so I can insert all items in one go overwriting the previous entries,
    // thus preventing screen flickering
    if (reset == true){
        document.getElementById("todo-items").innerHTML = todoContainer
    } else {
        document.getElementById("todo-items").innerHTML += todoContainer
    }
}

async function getTodo(status = false){
    let response = await fetch('get_todo/', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            status:status,
        }),
    }) // fetch

    return response.json()
}

function makeDraggable() {
    // Add drag functionality
    // Handles drag and drop events

    let todoList = document.getElementById("todo-items");
    var draggedItem = null
    var draggedItemStatus = false

    todoList.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', e.target.innerText);
        draggedItem = e.target;

        const status = e.target.querySelector('input[type="checkbox"]');
        draggedItemStatus = status.checked
    });

    todoList.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    todoList.addEventListener('drop', (e) => {
        e.preventDefault();

        // create the new element
        text = e.dataTransfer.getData('text/plain');
        let todoItem = createTodoElement(text, draggedItem.id, draggedItemStatus)
        
        // Determine the drop position based on the mouse cursor position
        let mouseY = e.clientY;
        let dropIndex = -1;
        let todoItems = todoList.querySelectorAll('li');

        todoItems.forEach((item, index) => {
            const rect = item.getBoundingClientRect();
            const itemY = (rect.top + rect.bottom) / 2;

            if (mouseY > itemY) {
                dropIndex = index + 1; // Drop below this item
            }
        });

        dropIndex = Math.max(0,dropIndex)
        todoList.insertBefore(todoItem, todoList.children[dropIndex]);

        draggedItem.remove();

        updateTaskOrder(todoList);
    });
}

function hideThis(toHide = false, toShow = false){
    // Helper function called directly from element, hides show finished tasks button
    
    if (toHide != false) {
        document.getElementById(toHide).style.display = "none";
    }

    if (toShow != false){
        document.getElementById(toShow).style.display = "block";
    }
}

function updateTaskOrder(todoList) {
    // Helper function.
    // Updates task order upon drop.
    // Converts index in array as displayed to position in django models.

    const taskItems = todoList.querySelectorAll('li');
    const taskIds = Array.from(taskItems).map((taskItem) => taskItem.id);
    
    fetch('reorder_todo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ taskIds }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to update task order');
            }
        })
        .catch((error) => {
            console.error(error);
        });
}

function checkboxHandler() {
    // Helper function.
    // Listens POSTs when checkbox is clicked or unclicked.

    let todoList = document.getElementById("todo-items");
    todoList.addEventListener('change', (e) => {
        updateStatus(e.target.id, e.target.checked)
    });
}

function updateStatus(todoId, status) {
    // Helper function for checkboxHandler, sends check/unchecked status to python for handling
    
    fetch('update_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            todoId: todoId,
            status: status,
        })
    })
}

function editButton(todoId) {
    // Shows popup edit button when ellipsis in todo list item is clicked

    // Hide all existing popups.
    let popups = document.querySelectorAll(".popuptext");
    popups.forEach((item) => {
        if (item.classList.contains("show") && item.id != "popup-"+todoId) {
            item.classList.toggle("show");
        }
    });

    // Show target
    var popup = document.getElementById(`popup-${todoId}`);
    popup.classList.toggle("show");
}

async function deleteThis(todoId) {
    
    // Delete entry
    let r = await fetch('delete_entry/', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            todoId:todoId
        })
    })
    const response = await r.json();

    // Refresh todo views
    if (document.getElementById("hide-finished-tasks").offsetParent === null){
        await showTodoAsList(false, true)
    } else {
        await showTodoAsList(null, true)
    }

}

function globalClickCatcher(){
    window.addEventListener('click', ({ target }) => {
        if (!target.classList.contains("fa-ellipsis")) {
            let popups = document.querySelectorAll(".popuptext");

            popups.forEach((item) => {
                if (item.classList.contains("show")) {
                    item.classList.toggle("show");
                }
            });
        }
    });

    // ISSUE: when clicking just outside of the ellipsis but still inside the span
    //        the span becomes the target, editButton still runs
}

// Edit button functionalities
function closeModalByEscape(event){
    if (event.key === "Escape") {
        closeEditModal();
    }
}

function closeEditModal(){
    console.log("closing")
    // Close modal
    modal = document.getElementById("modal-container");
    modal.removeAttribute("open");

    // Remove event listener
    document.removeEventListener("keydown", closeModalByEscape)
}

function autoGrow(element) {
    // Grows/shrinks textarea in edit modal.

    element.style.height = "5px";
    element.style.height = (element.scrollHeight) + "px";
  }

async function editThis(todoId){
    // Called when edit from popup menu is clicked.

    // Open modal
    modal = document.getElementById("modal-container");
    modal.setAttribute("open", true);

    // Set text
    textToEdit = document.getElementById(`text-entry-${todoId}`).innerText;
    editTextBox = document.getElementById("edit-todo-text");
    editTextBox.value = textToEdit;
    editTextBox.dispatchEvent(new Event('input', { bubbles: true })); // Simulates textarea input, to trigger oninput="autoGrow(this)"`
    document.getElementById("edited-todo-id").value = todoId;
    // Listen to escape key
    document.addEventListener("keydown", closeModalByEscape);
}

async function refreshView(){
    // Helper function

    // Refresh todo views
    if (document.getElementById("hide-finished-tasks").offsetParent === null){
        await showTodoAsList(false, true)
    } else {
        await showTodoAsList(null, true)
    }
}

async function postChanges(){
    // Called when save edit is initiated in the edit modal.
    // POSTs changes to django and closes the modal.

    editedTodo = document.getElementById("edit-todo-text").value;
    editedTodoId = document.getElementById("edited-todo-id").value;

    let r = await fetch('post_changes/', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            todoId:editedTodoId,
            editedTodo:editedTodo
        })
    })
    const response = await r.json();

    refreshView();
    closeEditModal();
}

// Main listener / caller
document.addEventListener('DOMContentLoaded', async function() {
    
    await showTodoAsList()
    makeDraggable()
    checkboxHandler()
    globalClickCatcher()

    // Listen for enter key on new todo
    document.getElementById("new-todo").addEventListener('keypress', function(event){
        if (event.key === "Enter") {
            event.preventDefault();
            newTodo()
        }
    })

    // Listen for enter key on edit todo
    document.getElementById("edit-todo-text").addEventListener('keypress', function(event){
        if (event.key === "Enter") {
            event.preventDefault();
            postChanges();
        }
    })
})