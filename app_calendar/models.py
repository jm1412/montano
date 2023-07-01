from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Calendar(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="todo")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    complete_by = models.DateTimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "todo": self.subject,
            "detail": self.body,
            "complete_by": self.complete_by.strftime("%b %d %Y, %I:%M %p"),
            "created_on": self.created_on.strftime("%b %d %Y, %I:%M %p")
        }
