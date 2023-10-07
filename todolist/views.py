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
    return render(request, "todolist/todo.html")

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
        todo=todo
    )
    todo.save()

    return HttpResponseRedirect(reverse('index'))


@require_POST
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
    

def get_todo(request):
    """ Returns all todo entries. """
    try:
        todo_items = Todo.objects.order_by("position").all()
        todo_list = [{'id': todo.id, 'item': todo.todo} for todo in todo_items]    
        return JsonResponse([todo.serialize() for todo in todo_items], safe=False)
    
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)