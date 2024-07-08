from django.urls import path
from ipon_goodbot import views

urlpatterns = [
    path("goodbot_postexpense/", views.gasto_new_entry, name="gasto_new_entry"),
    path("get_saved_timezones/", views.get_saved_timezones, name="get_saved_timezones")
]