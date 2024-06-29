from django.db import models

# Create your models here.
class Gasto(models.Model):
    telegram_id = models.CharField(max_length=255)
    amount_spent = models.IntegerField(default=0)
    date_spent = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)