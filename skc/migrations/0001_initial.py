# Generated by Django 4.2.2 on 2023-11-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=128)),
                ('customized', models.BooleanField(default=False)),
                ('type', models.TextField(max_length=24)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
            ],
        ),
    ]
