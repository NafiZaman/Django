# Generated by Django 3.1.2 on 2021-10-15 16:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2021, 10, 15, 16, 40, 18, 586352, tzinfo=utc)),
        ),
    ]