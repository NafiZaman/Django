# Generated by Django 3.1.2 on 2021-10-13 19:53

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211013_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_pic.svg', null=True),
        ),
    ]
