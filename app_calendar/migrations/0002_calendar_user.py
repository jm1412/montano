# Generated by Django 4.2.2 on 2023-09-05 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_calendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='todo', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
