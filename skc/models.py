from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()

# Create your models here.
skc_media_dir = os.path.join(settings.BASE_DIR,'skc/static/skc/media')

class Product(models.Model):
    name = models.CharField(max_length=128)
    customized = models.BooleanField(default=False) # false = regular cake, true = customized cake
    category = models.CharField(max_length=24, null=True ,choices=[
        ("regular","Regular"),
        ("mini","Mini"),
        ("bento","Bento"),
        ("bread-pastries","Bread & Pastries"),
        ("drinks","Drinks"),
        ("addons","Add-ons")
    ])
    type = models.CharField(max_length=24, null=True, choices=[
        ("birthday", "birthday"),
        ("christening","christening"),
        ("valentine","valentine"),
        ("wedding","wedding")
        ])
    image = models.ImageField(upload_to="images/") # jpeg
    price = models.IntegerField(default=0) # price to sell
    cost = models.IntegerField(default=0) # cost to make, calculated in views.py via production
    display = models.BooleanField(default=True) # if item is displayed on website
    date_added = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image.url,
            "customied": self.customized,
            "category": self.category,
            "type": self.type,
            "display": self.display
        }

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pos_entries")
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)

    def serialize(self):
        return {
            "user": self.user,
            "date": self.date,
            "total": self.total
        }
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
            # Calculate subtotal before saving
            self.subtotal = self.quantity * self.unit_price
            super().save(*args, **kwargs)

    def serialize(self):
        return{
            "sale": self.sale,
            "product": self.product,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal
        }