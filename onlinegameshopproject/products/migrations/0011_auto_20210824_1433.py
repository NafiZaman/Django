# Generated by Django 3.1.2 on 2021-08-24 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210822_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(limit_choices_to={'can_sell': True}, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]