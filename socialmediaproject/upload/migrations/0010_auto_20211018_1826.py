# Generated by Django 3.1.2 on 2021-10-18 16:26

from django.db import migrations, models
import upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0009_auto_20211016_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userupload',
            name='image',
            field=models.ImageField(default='abc_0101_11223.svg', upload_to=upload.models.user_directory_path),
        ),
    ]
