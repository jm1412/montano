# Generated by Django 4.2.2 on 2023-12-03 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skc', '0008_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('birthday', 'birthday'), ('christening', 'christening'), ('valentine', 'valentine'), ('wedding', 'wedding')], max_length=24),
        ),
    ]