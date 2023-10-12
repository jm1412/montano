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
    let new_todo = createTodoElement(todo, response.todo_id)
    let todo_list = document.getElementById("todo-items");
    todo_list.insertBefore(new_todo, todo_list.children[0]);

    updateTaskOrder(todo_list);
}

function createTodoElement(text, todo_id) {
    // Helper function
    // Creates new todo element

    let todo_item = document.createElement('li');
    todo_item.id = todo_id
    todo_item.classList.add("item-entry");
    todo_item.classList.add("list-unstyled");
    todo_item.innerHTML = `
        <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
        <label class="form-check-label" for="flexCheckDefault">
        ${text}
        </label>
    `
    todo_item.draggable = true;
    return todo_item
}

async function showTodo(){
    let response = await fetch('get_todo', {
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    }) // fetch

    let todo_items = await response.json();
    todo_items.forEach(function(todo_item){
        let element = document.createElement('div');
        element.className = "todo-item";
        element.id = todo_item.id;
        element.draggable = true;

        html =    `<div id="${todo_item.id}" class="row mx-1 my-2">
                        <div id="${todo_item.id}" class="item-entry card p-1">
                        ${todo_item.title}
                        </div>
                    </div>`

        element.innerHTML = html
        document.getElementById("todo-items").append(element)
    })
}

async function showTodoAsList(){
    let response = await fetch('get_todo', {
        method:'GET',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin'
    }) // fetch

    let todo_items = await response.json();
    todo_items.forEach(function(todo_item){
        let element = document.createElement('div');
        element.className = "todo-item";
        element.id = todo_item.id;
        element.draggable = true;

        // html =    `<li id="${todo_item.id}" class="item-entry">${todo_item.title}</li>`

        html = `
            <li id="${todo_item.id}" class="item-entry list-unstyled">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                <label class="form-check-label" for="flexCheckDefault">
                ${todo_item.title}
                </label>
            </li>
        `

        element.innerHTML = html
        document.getElementById("todo-items").append(element)
    })
}

function makeDraggable() {
    // Add drag functionality
    let todo_list = document.getElementById("todo-items");
    var draggedItem = null

    todo_list.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', e.target.innerText);
        draggedItem = e.target
    });

    todo_list.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    todo_list.addEventListener('drop', (e) => {
        e.preventDefault();

        // create the new element
        text = e.dataTransfer.getData('text/plain');
        let todo_item = createTodoElement(text, draggedItem.id)
        
        // Determine the drop position based on the mouse cursor position
        let mouseY = e.clientY;
        let dropIndex = -1;
        let todo_items = todo_list.querySelectorAll('li');

        todo_items.forEach((item, index) => {
            const rect = item.getBoundingClientRect();
            const itemY = (rect.top + rect.bottom) / 2;

            if (mouseY > itemY) {
                dropIndex = index + 1; // Drop below this item
            }
        });

        dropIndex = Math.max(0,dropIndex)
        todo_list.insertBefore(todo_item, todo_list.children[dropIndex]);

        draggedItem.remove();

        updateTaskOrder(todo_list);
    });
}

function updateTaskOrder(todo_list) {
    const taskItems = todo_list.querySelectorAll('li');
    const taskIds = Array.from(taskItems).map((taskItem) => taskItem.id);
    
    // Make an AJAX POST request to update the task order on the server
    fetch('reorder_todo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Make sure to include CSRF token
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
    let todo_list = document.getElementById("todo-items");
    todo_list.addEventListener('change', (e) => {
        
    });
}

// Main listener / caller
document.addEventListener('DOMContentLoaded', async function() {

    //showTodo()
    await showTodoAsList()
    makeDraggable()
    checkboxHandler()

})