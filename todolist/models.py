from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_entries")
    todo = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.todo
        }

class TodoRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_rank")
    rank = models.TextField()