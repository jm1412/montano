# Generated by Django 4.2.2 on 2023-12-20 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skc', '0012_alter_product_category_alter_product_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='skc.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
