# Generated by Django 4.2.2 on 2023-07-03 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_calendar', '0004_alter_calendar_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='year_highlight',
            field=models.BooleanField(default=False),
        ),
    ]