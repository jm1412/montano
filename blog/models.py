from django.db import models


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class BlogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_entries")
    blog_title = models.CharField(max_length=32, blank=False)
    blog_body = models.CharField(max_length=3200, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            "id": self.id,
            "title": self.blog_title,
            "body": self.blog_body,
            "posted_on": self.created_on
        }
    
