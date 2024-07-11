from django.db import models

# Create your models here.
class Gasto(models.Model):
    telegram_id = models.IntegerField()
    amount_spent = models.FloatField(default=0)
    date_spent = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    user_timezone = models.CharField(max_length=255)
    
    def serualize(self):
        return {
            "telegram_id": self.telegram_id,
            "amount_spent": self.amount_spent,
            "date_spent": self.date_spent,
            "created_on": self.created_on,
            "timezone": self.user_timezone
        }
    
class Timezone(models.Model):
    telegram_id = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255) # Europe/London
    
    def serialize(self):
        return {
            self.telegram_id: self.timezone,
        }
        
