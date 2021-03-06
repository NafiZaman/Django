# Generated by Django 3.1.2 on 2021-09-21 17:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210920_1549'),
        ('product', '0002_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=500)),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
