# Generated by Django 3.1.2 on 2021-09-01 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_stock_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='n_switch',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='pc',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='ps4',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='ps5',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='xbone',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='xbonex',
        ),
    ]