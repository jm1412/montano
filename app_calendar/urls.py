from django.urls import path
from app_calendar import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("year", views.year_view, name="year"),
    path("month", views.month_view, name="month"),
    path("test", views.test, name="test"),
    path(r"", views.calendarhome, name="calendarhome")
]