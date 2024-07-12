from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date
from django.conf import settings
import pytz

# Create your views here.
def request_authorized(request):
    auth_header = request.headers.get('Authorization')

    if auth_header != f"Bearer {settings.TELEGRAM_TOKEN}":
        return False
    return True
    
@csrf_exempt
def gasto_new_entry(request):
    """Create new entry."""
    if not request_authorized(request):
      return JsonResponse({"error": "Unauthorized"}, status=401)
        
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    amount_spent = data.get("amount", "")
    date_spent = data.get("date", "")
    timezone = data.get("timezone", "")
    
    datetime_obj = datetime.strptime(date_spent, "%Y-%m-%d")
    date_obj = datetime_obj.date()
    
    gasto = Expense(
        telegram_id = telegram_id,
        amount_spent = amount_spent,
        date_spent = date_obj,
        date_timezone = timezone
    )
    gasto.save()

    return JsonResponse({
        "message": "success"
    })
    
@csrf_exempt
def save_user_timezone(request):
    """Saves user timezone."""
    if not request_authorized(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    timezone = data.get("timezone", "")
    
@csrf_exempt
def get_saved_timezones(request):
    """Gets ALL users' timezones."""
    if not request_authorized(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    user_timezones = UserTimezone.objects.all()
    return JsonResponse([user_timezone.serialize() for user_timezone in user_timezones], safe=False)

@csrf_exempt
def save_user_timezone(request):
    """Save user timezone."""
    if not request_authorized(request):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id", "")
    timezone = data.get("timezone", "")

    new_timezone = UserTimezone(
        telegram_id = telegram_id,
        timezone = timezone
        )
    new_timezone.save()
    
    return JsonResponse({"message": "Success"}, status=200)

@csrf_exempt
def get_expenses_today(request):
    """ Returns all expense entries by user. """

    data = json.loads(request.body)
    status = data.get("status","")
    user = request.user

    try:
        if status == None:
            todo_items = Todo.objects.order_by("status", "position").filter(user=user)
        else:
            todo_items = Todo.objects.order_by("status", "position").filter(user=user, status=status)
        return JsonResponse([todo.serialize() for todo in todo_items], safe=False)
    
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

@csrf_exempt
def get_expense_amount_today(request):
    """Returns total expenses for today, adjusted by user timezone"""
    
    data = json.loads(request.body)
    telegram_id = data.get("telegram_id","")
    timezone = data.get("timezone", "")
    
    user_tz = pytz.timezone(timezone)
    date_spent = datetime.now(user_tz).date()
    
    user_expenses_today = Expense.objects.filter(telegram_id=telegram_id, date_spent=date_spent)
    
    expense_amount_today = 0
    for item in user_expenses_today:
        expense_amount_today += item.amount_spent

    return JsonResponse({"total":expense_amount_today})