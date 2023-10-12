from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required


from .models import *
import json

 
# Create your views here.
def todo_index(request):
    if request.user.is_authenticated:
        return render(request, "todolist/todo.html")
    else:
        return render(request, "shared/login.html", {
            "from_app":"todo_index"
        })

@login_required
@requires_csrf_token
def new_entry(request):
    print("creating new entry")

    """ Create post. """
    data = json.loads(request.body)
    todo = data.get("todo", "")
    user = request.user
    
    todo = Todo(
        user=user, 
        todo=todo,
        position=-1
    )
    todo.save()

    return JsonResponse({
        "todo_id":todo.id
    })

@login_required
@require_POST
@requires_csrf_token
def reorder_todo(request):
    try:
        data = json.loads(request.body)
        task_ids = data.get('taskIds', [])

        # Loop through the task IDs and update their positions
        for index, task_id in enumerate(task_ids):
            task = Todo.objects.get(pk=task_id)
            task.position = index
            task.save()

        return JsonResponse({'message': 'Tasks reordered successfully'}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@requires_csrf_token
def get_todo(request):
    """ Returns all todo entries. """
    user = request.user
    try:
        todo_items = Todo.objects.order_by("position").filter(user=user)
        todo_list = [{'id': todo.id, 'item': todo.todo} for todo in todo_items] # not used   
        return JsonResponse([todo.serialize() for todo in todo_items], safe=False)
    
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    

def update_status(request):
    """ Updates status of todolist items. """

    data = json.loads(request.body)
    todo_id = data.get("todo_id", "")
    status = data.get("status", "")
    user = request.user

    print(f"status: {status}, id: {todo_id}")
    
    todo = Todo.objects.get(
            user=user,
            id=todo_id
            )
    todo.status = status
    todo.save()

    return JsonResponse({'message': "status updated"})