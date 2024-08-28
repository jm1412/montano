from django.urls import path
from ipon_goodbot import views

urlpatterns = [
    path("goodbot_postexpense/", views.gasto_new_entry, name="gasto_new_entry"),
    path("get_saved_timezones/", views.get_saved_timezones, name="get_saved_timezones"),
    path("save_user_timezone/", views.save_user_timezone, name="save_user_timezone"),
    path("get_expense_amount_today/", views.get_expense_amount_today, name="get_expense_amount_today"),
    path("get_expenses/", views.get_expenses, name="get_expenses")
]


