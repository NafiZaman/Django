# Generated by Django 3.1.2 on 2021-10-19 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0010_auto_20211018_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userupload',
            old_name='image',
            new_name='image_path',
        ),
    ]
