# Generated by Django 3.1.2 on 2021-09-23 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20210922_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerproductreview',
            name='product_rating',
        ),
    ]
