from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from .models import *
import json

BLOGS_PER_PAGE = 10

# Create your views here.
def blog_index(request):
    """ Render main blog page. """
    return render(request, "blog/blog.html")

@require_GET
def get_blogs(request, page_number):
    """ Returns pagination of blog entries """
    print("get_blogs")

    entries = BlogEntry.objects.order_by("-created_on").all()
    paginator = Paginator(entries, BLOGS_PER_PAGE)
    page = paginator.page(page_number).object_list

    return JsonResponse([entry.serialize() for entry in page], safe=False)


    # notes
    if paginator.num_pages < int(request.GET.get('page')):
        return JsonResponse({})
    else:
        page = paginator.page(request.GET.get('page')).object_list
        return JsonResponse([entry.serialize() for entry in page], safe=False)


def number_of_pages(request):
    """ Returns number of pages for paginator. """

    entries = BlogEntry.objects.order_by("-created_on").all()
    paginator = Paginator(entries, BLOGS_PER_PAGE)
    
    return JsonResponse(paginator.num_pages, safe=False)

def open_blog(request, blog_id):
    """ Opens specific blog. """

    blog = BlogEntry.objects.get(id=blog_id)
    
    return render(request, "blog/blog_page.html", {
        "blog_title": blog.blog_title,
        "blog_body": blog.blog_body,
        "blog_posted_on": blog.created_on
    })