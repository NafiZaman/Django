# Generated by Django 3.1.2 on 2021-10-16 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20211016_1807'),
        ('users', '0010_auto_20211016_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ForeignKey(blank=True, default='default_pic.svg', null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload.userupload'),
        ),
    ]
