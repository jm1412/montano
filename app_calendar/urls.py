from django.urls import path
from app_calendar import views

urlpatterns = [
    path("", views.index, name="calendarhome"),
    #path("login", views.login, name="login"),
    path("year", views.year_view, name="year"),
    path("month", views.month_view, name="month"),
    path("test", views.test, name="test"),
    path(r"", views.calendarhome, name="calendarhome"),
    path("get_calendar_year/<int:current_year>", views.get_calendar_year, name="get_calendar_year"),
    path("get_calendar_month/<int:target>", views.get_calendar_month, name="get_calendar_month"),
    path("create_entry", views.create_entry, name="create_entry")
]