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
    console.log(`adding new todo: ${todo}`);

    await fetch('/new_entry', {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')},
        mode:'same-origin',
        body: JSON.stringify({
            todo:todo,
        })
    })

    document.getElementById("new-todo").value = "";
    
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

        html =    `<div class="row mx-1 my-2">
                        <div class="card p-1">
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

        html =    `<li id="item-entry">${todo_item.title}</li>`

        element.innerHTML = html
        document.getElementById("todo-items").append(element)
    })
}

function makeDraggable() {
    // Add drag functionality
    let todo_list = document.getElementById("todo-items");
    let todo_items = todo_list.querySelectorAll('li');
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
        let text = e.dataTransfer.getData('text/plain');
        let todo_item = document.createElement('li');
        todo_item.innerText = text;
        todo_item.draggable = true;
        
        // Determine the drop position based on the mouse cursor position
        const mouseY = e.clientY;
        let dropIndex = -1;
    
        todo_items.forEach((item, index) => {
            console.log(`todo_item: ${item}`)
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

    todo_list.removeEventListener();
    console.log("running")
}

function updateTaskOrder(todo_list) {
    makeDraggable()


    // const taskItems = todo_list.querySelectorAll('li');
    // const taskIds = Array.from(taskItems).map((taskItem) => taskItem.innerText);
    
    // // Make an AJAX POST request to update the task order on the server
    // fetch('/reorder_todo/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': getCookie('csrftoken'), // Make sure to include CSRF token
    //     },
    //     body: JSON.stringify({ taskIds }),
    // })
    //     .then((response) => {
    //         if (!response.ok) {
    //             throw new Error('Failed to update task order');
    //         }
    //     })
    //     .catch((error) => {
    //         console.error(error);
    //     });


}



// Main listener / caller
document.addEventListener('DOMContentLoaded', async function() {

    //showTodo()
    await showTodoAsList()
    makeDraggable()

})