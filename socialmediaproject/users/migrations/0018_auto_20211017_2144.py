# Generated by Django 3.1.2 on 2021-10-17 19:44

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20211017_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='abc_0101_11223.svg', upload_to=users.models.user_directory_path),
        ),
    ]
