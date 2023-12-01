from django.urls import path
from skc import views

urlpatterns = [
    path("", views.skc_index, name="skc_index"),
    path("regular-cakes", views.regular_cakes, name="regular_cakes"),
    path("customized-cakes", views.customized_cakes, name="customized_cakes"),
    path("get-customized-cakes/<int:page_number>", views.get_customized_cakes, name="get_customized_cakes"),
    path("number-of-pages", views.number_of_pages, name="number_of_pages")
]