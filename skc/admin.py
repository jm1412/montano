from django.contrib import admin
from .models import Product, Sale, SaleItem
from PIL import Image, ImageFilter, ImageOps
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        Overrides save function on admin panel, converts images to square and resizes to 1080px.
        """

        super().save_model(request, obj, form, change)

        if 'image' in form.changed_data:
            original_image = Image.open(obj.image.path)
            exif = original_image._getexif()

            # Rotate image
            orientation_key = 274 # cf ExifTags
            if exif and orientation_key in exif:
                orientation = exif[orientation_key]

                rotate_values = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90
                }

                if orientation in rotate_values:
                    original_image = original_image.transpose(rotate_values[orientation])

            # Blur image
            blur_image = original_image.filter(ImageFilter.GaussianBlur(radius=25))

            # Crop image
            width, height = blur_image.size   # Get dimensions
            left = round((width - 1080)/2)
            top = round((height - 1080)/2)
            x_right = round(width - 1080) - left
            x_bottom = round(height - 1080) - top
            right = width - x_right
            bottom = height - x_bottom
            blur_image = blur_image.crop((left, top, right, bottom))

            # Resize to 1080
            original_image = ImageOps.contain(original_image,(1080,1080))

            # Paste original image on top of blurred image
            width, height = original_image.size
            blur_image.paste(original_image,((1080-width)//2, (1080-height)//2))

            # Save the resized image back to the same file
            resized_image = blur_image.resize((1080,1080))
            resized_image.save(obj.image.path)

admin.site.register(Product,ProductAdmin)
admin.site.register(Sale)
admin.site.register(SaleItem)