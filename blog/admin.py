from django.contrib import admin
from .models import BlogEntry
from django import forms
from django.db import models

# Register your models here.
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_body')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'blog_body':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 4, 'cols': 40})
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(BlogEntry, BlogEntryAdmin)

