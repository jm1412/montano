from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class products(models.Model):
    name = models.TextField(max_length=128)
    customized = models.BooleanField(default=False) # false = regular cake, true = customized cake
    type = models.TextField(max_length=24) # cake, pastry, drinks, etc
    image = models.ImageField() # jpeg
    price = models.IntegerField(default=0) # price to sell
    cost = models.IntegerField(default=0) # cost to make, calculated in views.py via production