from django.urls import path
from blog import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("get_blogs/<int:page_number>", views.get_blogs, name="get_blogs"),
    path("number_of_pages", views.number_of_pages, name="number_of_pages"),
    path("show_blog/<int:blog_id>", views.show_blog, name="show_blog")
]