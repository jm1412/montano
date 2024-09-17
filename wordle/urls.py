from django.urls import path
from wordle import views

urlpatterns = [
    path('new/', views.new_wordle, name='new_wordle'),
    path('submit-guess/', views.submit_guess, name='submit_guess'),
]

