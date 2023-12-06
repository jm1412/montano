from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from skc.models import Product
from django.conf import settings
import os
from PIL import Image, ImageFilter, ImageOps

import json

# Create your views here.
POSTS_PER_PAGE = 9



def skc_index(request):
    return render(request, "skc/index.html")

def view_cakes(request, type):
    page_number = request.GET.get("page")

    # Get products
    if type == "customized":
        customized = True
    if type == "regular":
        customized = False

    # Query products
    query = Product.objects.order_by("-date_added").filter(customized=customized)
    paginator = Paginator(query, POSTS_PER_PAGE)
    page = paginator.page(page_number).object_list
    products = [product.serialize() for product in page]

    # Get pages
    try:
        paginated_queryset = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    return render(request, "skc/cakes.html", {"products":products,"page":page_number, 'paginated_queryset': paginated_queryset})

def get_cakes(type, page_number):
    """ Gets customized cakes and returns them. """
    if type == "customized":
        customized = True
    if type == "regular":
        customized = False

    products = Product.objects.order_by("-date_added").filter(customized=customized)
    paginator = Paginator(products, POSTS_PER_PAGE)
    page = paginator.page(page_number).object_list

    return page

def make_images_square(request):
    """ Makes all images in media/images square """
    products = Product.objects.filter(squared=False)

    if len(products) > 0:
        for product in products:
            target_image = product.image.path
            product.squared=True
            convert_to_square_with_centered_blurred_background(target_image,target_image)
            product.save()
    return render(request, "skc/index.html")

def resize_images(request):
    """ Makes all images in media/images 1080x1080px"""
    products = Product.objects.filter(squared=False)

    if len(products) > 0:
        for product in products:
            target_image = product.image.path
            original_image = Image.open(target_image)
            resized_image = original_image.resize((1080,1080))
            resized_image.save()
    return render(request, "skc/index.html")

# Image handler
def convert_to_square_with_centered_blurred_background(input_path, output_path):
    """
    Converts all uploaded image to square and adds a blurred background.
    Marks image as edited in models.
    """

    # Open the image using Pillow
    original_image = Image.open(input_path)

    # Blur the image
    blur_image = original_image.filter(ImageFilter.GaussianBlur(radius=25))

    # Crop the blurred image to square
    width, height = blur_image.size   # Get dimensions

    left = round((width - 1080)/2)
    top = round((height - 1080)/2)
    x_right = round(width - 1080) - left
    x_bottom = round(height - 1080) - top
    right = width - x_right
    bottom = height - x_bottom
    blur_image = blur_image.crop((left, top, right, bottom))

    # Resize original image to 1080 longest side
    original_image = ImageOps.contain(original_image,(1080,1080))

    # Paste original image on top of blurred image
    width, height = original_image.size
    blur_image.paste(original_image,((1080-width)//2, (1080-height)//2))

    # Save
    blur_image.save(output_path)