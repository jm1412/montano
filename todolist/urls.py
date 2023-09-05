from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.todo_index, name="todo_index")
]