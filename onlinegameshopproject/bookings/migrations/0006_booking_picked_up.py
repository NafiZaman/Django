# Generated by Django 3.1.2 on 2021-09-03 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_booking_is_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='picked_up',
            field=models.BooleanField(default=False),
        ),
    ]