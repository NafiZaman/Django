# Generated by Django 3.1.2 on 2021-09-03 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_booking_picked_up'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='picked_up',
            new_name='is_picked_up',
        ),
    ]
