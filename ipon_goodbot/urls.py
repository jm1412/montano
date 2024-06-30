from django.urls import path
from ipon_goodbot import views

urlpatterns = [
    path("goodbot_postexpense/", views.gasto_new_entry, name="gasto_new_entry"),
]