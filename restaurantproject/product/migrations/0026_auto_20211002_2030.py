# Generated by Django 3.1.2 on 2021-10-02 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20211002_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productreviewsentiment',
            old_name='product_review',
            new_name='review',
        ),
    ]
