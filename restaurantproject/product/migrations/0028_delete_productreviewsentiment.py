# Generated by Django 3.1.2 on 2021-10-02 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20211002_2032'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductReviewSentiment',
        ),
    ]