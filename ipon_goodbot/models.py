from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense_maker")
    telegram_id = models.IntegerField()
    amount_spent = models.FloatField(default=0)
    date_spent = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    date_timezone = models.CharField(max_length=255)
    expense_comment = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    
    def serialize(self):
        return {
            "telegram_id": self.telegram_id,
            "amount_spent": self.amount_spent,
            "date_spent": self.date_spent,
            "created_on": self.created_on, 
            "date_spent_timezone": self.date_timezone,
            "expense_comment": self.expense_comment,
            "category": self.category
        }
    
class UserTimezone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense_entries")
    telegram_id = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255) # Europe/London
    
    def serialize(self):
        return {
            self.telegram_id: self.timezone
        }