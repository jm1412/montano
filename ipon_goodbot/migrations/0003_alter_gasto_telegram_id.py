# Generated by Django 5.0.1 on 2024-07-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipon_goodbot', '0002_timezone_gasto_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='telegram_id',
            field=models.IntegerField(),
        ),
    ]
