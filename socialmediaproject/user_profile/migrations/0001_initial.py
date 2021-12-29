# Generated by Django 3.1.2 on 2021-10-18 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0010_auto_20211018_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('education', models.CharField(blank=True, max_length=250, null=True)),
                ('rel_status', models.CharField(blank=True, choices=[('single', 'single'), ('engaged', 'engaged'), ('married', 'married')], max_length=50, null=True)),
                ('work', models.CharField(blank=True, max_length=250, null=True)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('profile_pic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='upload.userupload')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
        ),
    ]