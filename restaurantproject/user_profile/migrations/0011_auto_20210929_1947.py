# Generated by Django 3.1.2 on 2021-09-29 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_auto_20210929_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='customer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='customer',
            new_name='user',
        ),
    ]
