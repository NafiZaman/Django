# Generated by Django 3.1.2 on 2021-10-19 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0011_auto_20211019_0610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userupload',
            old_name='image_path',
            new_name='image',
        ),
    ]
