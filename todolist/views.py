from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.
def todo_index(request):
    return render(request, "todolist/todo.html")

@login_required
def new_entry(request):
    print("creating new entry")


    """ Create post. """
    if request.method != "POST":
        return JsonResponse({"error":"POST request required"}, status=400)

    data = json.loads(request.body)
    user = request.user
    post = data.get("post", "")
    
    woof = Woof(
        user=user,
        post=post
    )
    woof.save()

    return HttpResponseRedirect(reverse('index'))
