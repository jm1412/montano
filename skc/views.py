import os
import json
from datetime import date
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

from skc.models import Product, Sale, SaleItem
from accounts.models import User

from PIL import Image, ImageFilter, ImageOps

# for report generation
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from tabulate import tabulate
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from io import BytesIO


# Create your views here.
POSTS_PER_PAGE = 9

def pos(request):
    if request.user.is_authenticated:
        return render(request,"skc/pos.html")
    else:
        return redirect("/login")

def pos_submit(request):
    data = json.loads(request.body)
    orders = data["orders"]
    print(orders)
    total = 0

    new_sale = Sale.objects.create(
        user = request.user
    )

    for item, details in orders.items():
        print(details["qty"])
        product = Product.objects.get(id=item)
        SaleItem.objects.create(
            sale = new_sale,
            product = product,
            quantity = details["qty"],
            unit_price = details["price"]
        )
        total +=  details["price"] * details["qty"]
    
    new_sale.total = total
    new_sale.save()
        
    return JsonResponse({'message': 'success'})

def skc_index(request):
    return render(request, "skc/index.html")

def get_products(request):
    products = Product.objects.all()

    return JsonResponse([product.serialize() for product in products], safe=False)

def skc_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, "skc/index.html")
        else:
            return render(request, "skc/login.html")

    else:
        return render(request, "skc/login.html")
    
def get_regular_cakes(request):
    regular_cakes = Product.objects.filter(category="regular")
    return [regular_cake.serialize() for regular_cake in regular_cakes]

def view_cakes(request, type):
    return render(request,"skc/cakes.html",{"type":type, "user": request.user})

    # Initially made it so that on load, renders and returns products. Decided to break it down to smaller chunks for readability and reusability.
    # Keeping this chunk of code for if and when I need to paginate the POS (i.e. too many items)

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

def get_one_image(request, type):
    page = request.GET.get('page','')
    return get_images(request,type,1,page)

def get_images(request, type, images_per_page=9, override_page=False):
    if not override_page:
        page_number = request.GET.get('page', 1)
    else:
        page_number = override_page

    customized = True if type == "customized" else False
    query = Product.objects.order_by("-date_added").filter(customized=customized)
    paginator = Paginator(query, images_per_page)
    page = paginator.page(page_number).object_list
    products = [product.serialize() for product in page]

    # Get pages
    try:
        paginated_queryset = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'data': [], 'has_next': False})


    products = [product.serialize() for product in page]
    data = {'products': products, 'has_next': paginated_queryset.has_next(), 'has_previous': paginated_queryset.has_previous(), 'max_pages':paginator.num_pages}
    return JsonResponse(data)

def get_cakes(type, page_number):
    """ Gets cakes and returns them. """
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

# Report generator
def create_pdf_from_dict(table, from_date, to_date, user):
  
    filename = "sales_report.pdf"
    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Set font
    pdf_canvas.setFont("Helvetica", 8)

    # Add content to the PDF
    pdf_canvas.drawString(100, 800, f"Sales Report by {table[0][0]}")
    pdf_canvas.drawString(100, 785, f"Username: {user.username}")
    pdf_canvas.drawString(100, 770, f"Date: {from_date} to {to_date}")
    pdf_canvas.drawString(100, 755, "-" * 50)
            
    t=Table(table)
    style = TableStyle([('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                    ])  # (startCol, startRow), (endCol, endRow)
    t.setStyle(style)
    t.wrapOn(pdf_canvas,550,750)
    w, h = t.wrap(0,0)
    
    t.drawOn(pdf_canvas,((550-w)/2),750-h)

    # Save the PDF
    pdf_canvas.save()
    pdf_buffer.seek(0)

    return pdf_buffer

def prepare_by_product_table(sales, report_type):
    total = 0

    if report_type == "by_product":
        table = [["ID","Product","Quantity","Unit Price","Total"]]
        
        for sale in sales:
            for index, item in enumerate(table):
                # Checks every item in table, if item not in table, append
                if sale.product.id == item[0]:
                    table[index][2] += sale.quantity
                    table[index][4] += sale.subtotal
                    total += sale.subtotal
                    break
                
                elif index+1 == len(table):
                    table.append([
                        sale.product.id,
                        sale.product.name,
                        sale.quantity,
                        sale.unit_price,
                        sale.subtotal
                    ])
                    total += sale.subtotal
                    break # add break because if I don't the for loop runs once more because there's a new item
        table.append(["","","","",total])
    elif report_type == "by_category":
        table = [["Category","Quantity","Unit Price","Total"]]

        for sale in sales:
            custom_category = f"{sale.product.category}-{sale.unit_price}"
            
            for index, item in enumerate(table):
                if custom_category == item[0]:
                    table[index][1] += sale.quantity
                    table[index][3] += sale.subtotal
                    total += sale.subtotal
                    break
                
                elif index+1 == len(table):
                    table.append([
                        custom_category,
                        sale.quantity,
                        sale.unit_price,
                        sale.subtotal
                    ])
                    total += sale.subtotal
        table.append(["","","",total])
    return table

def generate_pdf(report_type, from_date, to_date, user):
    """ Main function for report generation. """
    
    from_date = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=None)
    to_date = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=None) + timedelta(days=1)
    
    sales = SaleItem.objects.filter(sale__date__range=(from_date, to_date)).filter(sale__user=user)
    table = prepare_by_product_table(sales, report_type)
    pdf_buffer = create_pdf_from_dict(table, from_date, to_date, user)

    # Create a response with the PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'
    response.write(pdf_buffer.read())

    return response

def pos_reports(request):
    """ 
    Gets called on page load. 
    Decides wether or not to generate the report.
    """
    report_type = request.GET.get("reportType")
    from_date = request.GET.get("reportFromDate")
    to_date = request.GET.get("reportToDate")
    user = request.user
    
    if(report_type == None or from_date == None or to_date == None):
        return render(request, "skc/reports.html")
    else:
        return generate_pdf(report_type, from_date, to_date, user)