import random
import string
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WordleGame
five_letter_words = [
    "apple", "brave", "clean", "drive", "eagle", "frame", "grape", "house",
    "jolly", "knife", "lucky", "magic", "noble", "ocean", "peace", "quick",
    "round", "shine", "table", "unity", "vivid", "whale", "xerox", "yield",
    "zebra", "actor", "beach", "charm", "dance", "eager", "flame", "globe",
    "happy", "ideal", "joker", "karma", "large", "mount", "nurse", "opera",
    "party", "quiet", "river", "stone", "train", "urban", "voter", "wrist",
    "xenon", "yacht", "zonal", "angel", "brisk", "crisp", "doubt", "early",
    "flood", "group", "heart", "index", "joint", "kneel", "light", "metal",
    "never", "orbit", "pilot", "quest", "reach", "skill", "trust", "upper",
    "valid", "waste", "young", "zesty", "alien", "birth", "close", "dream",
    "event", "flock", "giant", "hobby", "input", "judge", "kiosk", "learn",
    "march", "night", "overt", "pride", "range", "scary", "tiger", "unite",
    "voice", "watch", "xerox", "yield", "zonal", "alarm", "brave", "close",
    "dress", "eagle", "flame", "glare", "hatch", "inner", "jolly", "knock",
    "laugh", "minor", "noble", "offer", "proud", "quiet", "raise", "shock",
    "tight", "upset", "value", "whale", "xerox", "yacht", "zonal", "above",
    "baker", "claim", "draft", "eager", "flask", "great", "hover", "inbox",
    "jumpy", "knelt", "level", "march", "never", "other", "pulse", "reply",
    "sharp", "tough", "upper", "vital", "waste", "youth", "zonal", "angle",
    "bingo", "candy", "drown", "empty", "frost", "grasp", "hover", "intro",
    "jolly", "knelt", "layer", "march", "nicer", "organ", "pause", "quilt",
    "raven", "smart", "tasty", "under", "vivid", "watch", "xenon", "youth",
    "zones", "alert", "bring", "chill", "depth", "equal", "flash", "great",
    "happy", "input", "joint", "knack", "lucky", "medal", "nurse", "order",
    "place", "quiet", "robot", "slide", "trace", "until", "vital", "worse",
    "xenon", "yummy", "zones", "admit", "blend", "crowd", "drama", "early",
    "flora", "grape", "honey", "image", "joker", "kneel", "lover", "metal",
    "nicer", "offer", "pride", "quest", "river", "smart", "tiger", "unite",
    "value", "whisk", "xenon", "yummy", "zones", "agree", "bonus", "charm",
    "dodge", "entry", "focus", "grill", "house", "intro", "jolly", "kneel",
    "laser", "match", "never", "offer", "pride", "queue", "robot", "shift",
    "total", "urban", "vivid", "wrist", "xenon", "youth", "zones", "alien",
    "beard", "crisp", "drown", "early", "fruit", "green", "honey", "ideal",
    "joker", "kneel", "lemon", "march", "night", "offer", "pause", "quest",
    "reach", "smart", "total", "unity", "vivid", "whisk", "youth", "zones",
    "after", "blend", "crane", "ditch", "empty", "globe", "heart", "jumpy",
    "kneel", "learn", "mount", "ocean", "piano", "quiet", "ridge", "slide",
    "train", "upper", "value", "whale", "xenon", "yummy", "zones", "alert",
    "brave", "creep", "drain", "equal", "flame", "great", "inbox", "jolly",
    "kneel", "lemon", "match", "nicer", "overt", "pause", "quiet", "river",
    "slide", "total", "unite", "vivid", "whisk", "xenon", "zones", "alien",
    "bring", "catch", "drive", "eagle", "flame", "group", "hover", "image",
    "joker", "kneel", "laser", "march", "nurse", "offer", "pause", "quiet",
    "reach", "shock", "train", "upper", "vital", "whisk", "xenon", "youth",
    "zones", "about", "angel", "beach", "brisk", "chill", "crane", "draft",
    "eager", "flora", "grasp", "house", "input", "joker", "kneel", "lemon",
    "match", "night", "offer", "piano", "quiet", "ridge", "smart", "total",
    "unity", "value", "wrist", "xenon", "yummy", "zones", "agree", "bingo",
    "crane", "ditch", "equal", "flame", "grasp", "hover", "intro", "jolly",
    "kneel", "learn", "march", "nurse", "offer", "piano", "quiet", "reach",
    "smart", "train", "under", "vivid", "whisk", "xenon", "zones", "after",
    "blend", "crisp", "ditch", "early", "fruit", "great", "hover", "image",
    "joker", "kneel", "lemon", "match", "night", "offer", "pause", "quest",
    "river", "shock", "train", "upper", "value", "whisk", "xenon", "zones",
    "alien", "brisk", "creep", "drain", "equal", "globe", "heart", "joker",
    "kneel", "laser", "march", "night", "offer", "piano", "quiet", "ridge",
    "slide", "total", "unity", "vital", "whisk", "xenon", "zones", "alien",
    "bring", "catch", "draft", "equal", "flora", "green", "hover", "ideal",
    "joker", "kneel", "lemon", "march", "nurse", "ocean", "piano", "quiet",
    "reach", "shock", "train", "upper", "value", "whale", "xenon", "zones"
]

# Dictionary to store tokens and associated words
word_tokens = {}

@csrf_exempt
def new_wordle(request):
    """View function to generate a new Wordle word and token."""
    if request.method == 'GET':
        try:
            # Generate a new token and select a random word
            token = str(random.randint(100000, 999999))
            selected_word = random.choice(five_letter_words)

            # Store the word associated with the token
            word_tokens[token] = selected_word

            # Return the selected word and token as JSON
            print(f"selected_word: {selected_word}")
            return JsonResponse({'word': selected_word, 'token': token})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def submit_guess(request):
    """View function to validate a Wordle guess."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            guess = data.get('guess')
            token = data.get('token')
            # Validate the guess and token
            if guess and len(guess) == 5 and token in word_tokens:
                correct_word = word_tokens[token]
                feedback = get_feedback(guess, correct_word)

                # Check if the guess is correct
                is_correct = guess == correct_word

                # Return feedback and correctness status as JSON
                return JsonResponse({'feedback': feedback, 'correct': is_correct})

            return JsonResponse({'error': 'Invalid guess or token.'}, status=400)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid request data.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def get_feedback(guess, correct_word):
    """Generate feedback for the guessed word."""
    guess = guess.lower()
    print(f"correct_word: {correct_word}, guess: {guess}")
    feedback = []
    for g, c in zip(guess, correct_word):
        if g == c:
            feedback.append("correct")
        elif g in correct_word:
            feedback.append("present")
        else:
            feedback.append("absent")
    print(f"feedback: {feedback}")
    return feedback