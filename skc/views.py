from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

import json
# Create your views here.

def skc_index(request):
    return render(request,"skc/index.html")
