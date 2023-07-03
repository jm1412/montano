from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *

import json
from django.http import JsonResponse

import logging # to allow console.log

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

# API for creating new calendar entries 
def create_entry(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request requried."}, status=400)
    
    data = json.loads(request.body)
    user = request.user
    todo = data.get("subject", "")
    detail = data.get("body", "")
    complete_by = data.get("complete_by", "")
    year_highlight = data.get("year_highlight", "")
    write_type = data.get("write_type", "")
                          
    if write_type == "new":
        todo = Calendar(
            user=user,
            todo=todo,
            detail=detail,
            complete_by=complete_by,
            year_highlight=True
        )
        todo.save()
    elif write_type == "edit":
        target = Calendar.objects.get(user=user, complete_by=complete_by, year_highlight=True)
        target.todo = todo
        target.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

def get_calendar_year(request):
    logger = logging.getLogger('app_api')
    logger.info(f"Getting calendar for user: {request.user}")

    query_year = 2023 # for testing purposes, final code should accept year as entry
    # TODO: add to filter if it is a year highlight or not
    
    # get all todolist
    user = User.objects.get(email=request.user) # get user.id
    entries = Calendar.objects.filter(user=user.id, complete_by__year=query_year) # get all calendar entries of user

    return JsonResponse([entry.yearview() for entry in entries], safe=False)
