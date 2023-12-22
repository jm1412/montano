from django.urls import path
from skc import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path("", views.skc_index, name="skc_index"),
    path("cakes/<str:type>", views.view_cakes, name="view_cakes"),
    path("make-images-square", views.make_images_square, name="make_images_square"),
    path("resize-images", views.resize_images, name="resize_images"),
    path("get-images/<str:type>", views.get_images, name="get_images"),
    path("get-one-image/<str:type>", views.get_one_image, name="get_one_image"),
    path('admin/', admin.site.urls),
    path("login", views.skc_login, name="skc_login"),
    path("pos", views.pos, name="pos"),
    path("get-products", views.get_products, name="get_products"),
    path("pos-submit", views.pos_submit, name="pos_submit")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)