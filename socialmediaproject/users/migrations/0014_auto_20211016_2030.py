# Generated by Django 3.1.2 on 2021-10-16 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_profile_interests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='job_status',
            new_name='work',
        ),
    ]