# Generated by Django 3.1.2 on 2021-10-01 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20211001_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('incomplete', 'incomplete'), ('confirmed', 'confirmed'), ('complete', 'complete')], default='incomplete', max_length=50),
        ),
    ]
