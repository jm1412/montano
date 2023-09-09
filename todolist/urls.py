from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.todo_index, name="todo_index"),
    path("new_entry", views.new_entry, name="todo_new_entry")
]