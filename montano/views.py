from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

def apps_index(request):
    return render(request, "shared/apps.html")

def index(request):
    return render(request, "shared/index.html")

def shared_login(request):
    """ 
    Handles sitewide login. 
    Called from individual apps, and returns user to whichever app they intially were in.

    from_app is a string which represents the name in urls.py which represents the index of app that called the shared_login

    from_app is called on get, and is a hidden input field on the login.html which gets included in post.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        from_app = request.POST["from_app"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(from_app))
        else:
            return render(request, "shared/login.html", {
                "message": "Invalid email and/or password",
                "from_app": from_app
            })

    else:
        data = json.loads(request.body)
        from_app = data.get("from_app", "") # where to return after login

        return render(request, "shared/login.html", {
            "from_app" : from_app
        })