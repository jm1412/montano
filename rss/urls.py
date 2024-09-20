from django.urls import path
from rss import views

urlpatterns = [
    path('mangapark/', views.scrape_mangapark, name='scrape_mangapark'),
]
