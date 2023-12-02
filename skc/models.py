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
    type = models.CharField(max_length=24) # cake, pastry, drinks, etc
    image = models.ImageField(upload_to="images/") # jpeg
    price = models.IntegerField(default=0) # price to sell
    cost = models.IntegerField(default=0) # cost to make, calculated in views.py via production
    squared = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "name": self.name,
            "price": self.price,
            "image": self.image.url
        }

