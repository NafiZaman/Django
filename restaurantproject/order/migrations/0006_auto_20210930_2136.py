# Generated by Django 3.1.2 on 2021-09-30 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210930_2135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
    ]
