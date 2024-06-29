from django.shortcuts import render
from .models import *

# Create your views here.
def gasto_new_entry(request):
    """Create new entry."""
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    amount_spent = data.get("amount", "")
    #date_spent = data.get("date", "")

    gasto = Gasto(
        telegram_id = telegram_id,
        amount_spent = amount_spent
    )
    gasto.save()

    return JsonResponse({
        "message": "success"
    })