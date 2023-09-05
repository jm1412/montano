from django.contrib import admin
from .models import *
from accounts.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Calendar)