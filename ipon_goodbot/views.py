from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date

# Create your views here.
@csrf_exempt
def gasto_new_entry(request):
    """Create new entry."""
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    amount_spent = data.get("amount", "")
    date_spent = data.get("date", "")
    
    datetime_obj = datetime.strptime(date_spent, "%Y-%m-%d")
    date_obj = datetime_obj.date()
    
    gasto = Gasto(
        telegram_id = telegram_id,
        amount_spent = amount_spent,
        date_spent = date_obj
    )
    gasto.save()

    return JsonResponse({
        "message": "success"
    })