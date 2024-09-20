from django.urls import path
from rss import views

urlpatterns = [
    path('mangapark/', views.mangapark_rss, name='mangapark_rss'),
    path('mangapark/<str:filter>/', views.mangapark_rss, name='mangapark_rss_filtered'),
]
