# Generated by Django 3.1.2 on 2021-10-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_auto_20211031_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
