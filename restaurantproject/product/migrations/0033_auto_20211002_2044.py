# Generated by Django 3.1.2 on 2021-10-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_productreviewsentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreviewsentiment',
            name='sentiment',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
