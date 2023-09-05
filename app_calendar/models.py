from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo")
    todo = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, blank=True)
    complete_by = models.DateTimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    year_highlight = models.BooleanField(default=False)

    def yearview(self):
        return {
                "id": self.id,
                "complete_by": self.complete_by.strftime("%Y-%m-%d"),
                "complete_time": self.complete_by.strftime("%I:%M %p"),
                "todo": self.todo,
                "detail": self.detail,
                "year_highlight": self.year_highlight
                # "user": self.user.email
            }