from django.urls import path
from blog import views

urlpatterns = [
    path("", views.blog_index, name="skc_index"),
]