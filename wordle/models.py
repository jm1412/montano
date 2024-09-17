from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class WordleGame(models.Model):
    """Model to store the state of a Wordle game."""
    token = models.CharField(max_length=64, unique=True)  # Unique token for the game session
    target_word = models.CharField(max_length=5, blank=True, null=True)  # Target word for the game
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the game was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the game was last updated

    def __str__(self):
        return f"Game {self.token}"