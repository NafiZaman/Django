# Generated by Django 3.1.2 on 2021-08-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210818_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='n_switch',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='pc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='ps4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='ps5',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='xbone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='xbonex',
            field=models.BooleanField(default=False),
        ),
    ]
