from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from accounts.models import User
from django.db import IntegrityError


def apps_index(request):
    return render(request, "shared/apps.html")

def index(request):
    return render(request, "shared/index.html")

def login_view(request, from_app=False):
    """ 
    Handles sitewide login. 
    Called from individual apps, and returns user to whichever app they intially were in.

    from_app is a string which represents the name in urls.py which represents the index of app that called the shared_login

    from_app is called on get, and is a hidden input field on the login.html which gets included in post.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if not from_app:
            from_app = request.POST["from_app"]

        user = authenticate(request, username=email, password=password)
        if user is not None:

            login(request, user)
            return redirect("/"+from_app)
        else:
            return render(request, "shared/login.html", {
                "message": "Invalid email and/or password",
                "from_app": from_app
            })

    else:
        return render(request, "shared/login.html", {
            "from_app" : from_app
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request, from_app=False):
    if request.method == "POST":
        email = request.POST["email"]

        if not from_app:
            from_app = request.POST["from_app"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["password-again"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                )
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return redirect("/"+from_app)
    else:
        return render(request, "shared/register.html", {
            "from_app": from_app
        })