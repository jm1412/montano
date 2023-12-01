from django.urls import path
from skc import views

urlpatterns = [
    path("", views.skc_index, name="skc_index"),
    path("regular-cakes", views.regular_cakes, name="regular_cakes"),
    path("customized-cakes", views.customized_cakes, name="customized_cakes"),
    path("get-cakes/<str:type>/<int:page_number>", views.get_cakes, name="get_cakes"),
    path("number-of-pages", views.number_of_pages, name="number_of_pages"),
    path("make-images-square", views.make_images_square, name="make_images_square")
]