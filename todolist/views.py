from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required


from .models import *
import json

 
# Create your views here.
def todo(request):
    if request.user.is_authenticated:
        return render(request, "todolist/todo.html")
    else:
        return redirect("/login/todo")

@login_required
@requires_csrf_token
def new_entry(request):
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
        "todoId":todo.id
    })

@login_required
@require_POST
@requires_csrf_token
def reorder_todo(request):
    """ Reorder position of todolist entries on drag and drop. """

    user = request.user

    try:
        data = json.loads(request.body)
        task_ids = data.get('taskIds', [])

        # Loop through the task IDs and update their positions
        for index, task_id in enumerate(task_ids):
            task = Todo.objects.get(pk=task_id)

            # Check if user is only editing tasks they own.
            if task.user != user:
                return JsonResponse({'message': 'You can only edit tasks that you own.'}, status=200)

            task.position = index
            task.save()

        return JsonResponse({'message': 'Tasks reordered successfully'}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@requires_csrf_token
def get_todo(request):
    """ Returns all todo entries. """

    data = json.loads(request.body)
    status = data.get("status","")
    user = request.user

    try:
        if status == None:
            todo_items = Todo.objects.order_by("status", "position").filter(user=user)
        else:
            todo_items = Todo.objects.order_by("status", "position").filter(user=user, status=status)
        return JsonResponse([todo.serialize() for todo in todo_items], safe=False)
    
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
@login_required
@requires_csrf_token
def update_status(request):
    """ Updates status of todolist items. """

    data = json.loads(request.body)
    todo_id = data.get("todoId", "")
    status = data.get("status", "")
    user = request.user
    
    todo = Todo.objects.get(
            user=user,
            id=todo_id
            )
    todo.status = status
    todo.save()

    return JsonResponse({'message': 'status updated'})

@login_required
@requires_csrf_token
@require_POST
def delete_entry(request):
    data = json.loads(request.body)
    todo_id = data.get("todoId","")
    user = request.user

    todo = Todo.objects.get(
        user=user,
        id=todo_id
    )
    todo.delete()

    return JsonResponse({'message': 'entry deleted'})

@login_required
def post_changes(request):
    data = json.loads(request.body)
    todo_id = data.get("todoId", "")
    edited_todo = data.get("editedTodo", "")
    user = request.user
    

    todo = Todo.objects.get(
        user=user,
        id=todo_id
    )
    todo.todo = edited_todo
    todo.save()

    return JsonResponse({'message': 'changes saved'})