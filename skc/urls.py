from django.urls import path
from skc import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.skc_index, name="skc_index"),
    path("cakes/<str:type>", views.view_cakes, name="view_cakes"),
    path("number-of-pages", views.number_of_pages, name="number_of_pages"),
    path("make-images-square", views.make_images_square, name="make_images_square"),
    path("resize-images", views.resize_images, name="resize_images")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)