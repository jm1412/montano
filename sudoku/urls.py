from django.urls import path
from sudoku import views

urlpatterns = [
    path('create-sudoku/<int:numbers_to_remove>/', views.create_sudoku_puzzle, name='create_sudoku'),
    path('validate-sudoku/', views.validate_sudoku_board, name='validate_sudoku')
]

