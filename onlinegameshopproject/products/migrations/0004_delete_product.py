# Generated by Django 3.1.2 on 2021-08-15 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_box_art'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
