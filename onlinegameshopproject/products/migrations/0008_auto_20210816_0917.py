# Generated by Django 3.1.2 on 2021-08-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210816_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='quantity',
        ),
        migrations.AddField(
            model_name='stock',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
