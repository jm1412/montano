from django.urls import path
from skc import views

urlpatterns = [
    path("", views.skc_index, name="skc_index"),
]