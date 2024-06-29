from django.shortcuts import render
from .models import *

# Create your views here.
def new_entry(request):
    """Create new entry."""
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    amount_spent = data.get("amount_spent", "")
    date_spent = data.get("date_spent", "")

    gasto = Gasto(
        telegram_id = telegram_id,
        amount_spent = amount_spent,
        date_spent = date_spent
    )
    gasto.save()

    return JsonResponse({
        "message": "success"
    })