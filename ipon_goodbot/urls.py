from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.todo, name="todo"),
    path("goodbot_postexpense/", views.gasto_new_entry, name="gasto_new_entry"),
]