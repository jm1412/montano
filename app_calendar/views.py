from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *

# Create your views here.
def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return HttpResponseRedirect("year")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app_calendar/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "app_calendar/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
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
                first_name = first_name,
                last_name = last_name
                )
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

@login_required
def year_view(request):
    if request.user.is_authenticated == False:
        return render(request, "app_calendar/index.html")
    return render(request, "app_calendar/year.html")


@login_required
def month_view(request):
    if request.user.is_authenticated == False:
        return render(request, "app_calendar/index.html")
    return render(request, "app_calendar/month.html")

def test(request):
    return render(request, "app_calendar/layout.html")

def calendarhome(request):
    return render(request, "app_calendar/year.html")