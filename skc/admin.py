from django.contrib import admin
from .models import Product
from PIL import Image, ImageFilter, ImageOps
# Register your models here.

# # admin.py
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Call the save_model method of the parent class
        super().save_model(request, obj, form, change)

        # Check if the image field has changed
        if 'image' in form.changed_data:
            # Open the uploaded image using Pillow
            original_image = Image.open(obj.image.path)

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

            # Save the resized image back to the same file
            blur_image.save(obj.image.path)

admin.site.register(Product,ProductAdmin)

