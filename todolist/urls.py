from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.todo_index, name="todo_index"),
    path("new_entry", views.new_entry, name="todo_new_entry"),
    path("reorder_todo/", views.reorder_todo, name="reorder_todo"),
    path("get_todo/", views.get_todo, name="get_todo")
]