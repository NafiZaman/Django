# Generated by Django 3.1.2 on 2021-08-14 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_newuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='shop_name',
        ),
    ]
