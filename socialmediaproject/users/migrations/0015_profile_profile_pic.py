# Generated by Django 3.1.2 on 2021-10-16 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20211016_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='abc_0101_11223.svg', upload_to=''),
        ),
    ]
