from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def gasto_new_entry(request):
    """Create new entry."""
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    amount_spent = data.get("amount", "")
    date_spent = data.get("date", "")
    gasto = Gasto(
        telegram_id = telegram_id,
        amount_spent = amount_spent
    )
    gasto.save()

    return JsonResponse({
        "message": "success"
    })