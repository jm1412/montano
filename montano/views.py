from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def apps_index(request):
    return render(request, "shared/apps.html")