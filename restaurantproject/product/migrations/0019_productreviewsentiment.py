# Generated by Django 3.1.2 on 2021-09-25 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210920_1549'),
        ('product', '0018_auto_20210925_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReviewSentiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentiment', models.CharField(default=None, max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
                ('product_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productreview')),
            ],
        ),
    ]
