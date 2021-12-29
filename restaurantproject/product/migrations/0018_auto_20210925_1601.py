# Generated by Django 3.1.2 on 2021-09-25 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210920_1549'),
        ('product', '0017_auto_20210925_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=500)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomerProductReview',
        ),
    ]
