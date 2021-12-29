# Generated by Django 3.1.2 on 2021-10-02 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0031_delete_productreviewsentiment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReviewSentiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentiment', models.CharField(default=None, max_length=50)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productreview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
        ),
    ]