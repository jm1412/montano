from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime
from .models import *

import json
from django.http import JsonResponse

import logging # to allow console.log

import pyrebase

config = {
  "apiKey": "AIzaSyAbU1s1A5DOaePZQqGmErjsekQ9kX2tHqo",
  "authDomain": "kalendaryo-6a451.firebaseapp.com",
  "databaseURL": "https://kalendaryo-6a451-default-rtdb.firebaseio.com",
  "storageBucket": "kalendaryo-6a451.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#db = firebase.database()
#storage=firebase.storage()

# Create your views here.
def index(request):
    # logger = logging.getLogger('app_api')
    # logger.info("---------------------- START -----------------------")
    # logger.info(request.META)
    # logger.info("--------------------- SESSION ---------------------")
    # logger.info(request.session)

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return HttpResponseRedirect("year")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
    
def login_view(request):
    logger = logging.getLogger('app_api')

    if request.method == "POST":
    
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.sign_in_with_email_and_password(email, password)

        # Check if authentication successful
        if user is not None:
            logger.info(user)
            #login(request, user)
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
    logger = logging.getLogger('app_api')

    if request.method != "POST":
        return JsonResponse({"error": "POST request requried."}, status=400)
    
    data = json.loads(request.body)
    id = data.get("id","")
    user = request.user
    todo = data.get("todo", "")
    detail = data.get("detail", "")
    complete_by = data.get("complete_by", "")
    complete_time = data.get("complete_time", "12:00 AM")
    year_highlight = data.get("year_highlight", "")
    write_type = data.get("write_type", "")

    # convert 12h to 24h
    complete_time = datetime.strptime(complete_time, "%I:%M %p")
    complete_time = datetime.strftime(complete_time, "%H:%M")
    complete_by = complete_by + " " + complete_time



    # year view writes
    if write_type == "new":
        todo = Calendar(
            user=user,
            todo=todo,
            detail=detail,
            complete_by=complete_by,
            year_highlight=year_highlight
        )
        todo.save()
    elif write_type == "edit":
        target = Calendar.objects.get(id=id)
        if len(todo) > 0:
            target.todo = todo
            target.save()
        elif len(todo) == 0:
            target.delete()
        
    elif write_type == "update": # used by month view
        target = Calendar.objects.get(id=id) # TODO: year highlight is missin for now
        target.todo = todo
        target.detail = detail
        target.complete_by = complete_by
        target.save()

    elif write_type == "delete":
        target = Calendar.objects.get(id=id) # TODO: needs more filters
        target.delete()
        
    return JsonResponse({"message": "Email sent successfully."}, status=201)

def get_calendar_year(request, current_year):
    logger = logging.getLogger('app_api')
    logger.info(f"Getting calendar for user: {request.user}")
    
    # get all todolist
    user = User.objects.get(email=request.user) # get user.id
    entries = Calendar.objects.filter(user=user.id, complete_by__year=current_year, year_highlight=True) # get all calendar entries of user

    return JsonResponse([entry.yearview() for entry in entries], safe=False)

def get_calendar_month(request, target):
    # target is yyyym
    target = str(target)

    user = User.objects.get(email=request.user)
    current_year = int(target[0:4])
    current_month = int(target[4:])

    entries = Calendar.objects.filter(
        user=user.id,
        complete_by__year=current_year,
        complete_by__month=current_month).order_by('complete_by')
    
    return JsonResponse([entry.yearview() for entry in entries], safe=False)