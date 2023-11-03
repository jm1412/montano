from django.urls import path
from todolist import views

urlpatterns = [
    path("", views.todo, name="todo"),
    path("new_entry/", views.new_entry, name="todo_new_entry"),
    path("delete_entry/", views.delete_entry, name="todo_delete_entry"),
    path("reorder_todo/", views.reorder_todo, name="reorder_todo"),
    path("get_todo/", views.get_todo, name="get_todo"),
    path("update_status/", views.update_status, name="update_status"),
    path("post_changes/", views.post_changes, name="post_changes")
]