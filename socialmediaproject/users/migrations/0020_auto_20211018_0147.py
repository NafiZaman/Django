# Generated by Django 3.1.2 on 2021-10-17 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20211017_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='abc_0101_11223.svg', null=True, upload_to=''),
        ),
    ]
