# Generated by Django 4.2.2 on 2023-12-01 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skc', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
