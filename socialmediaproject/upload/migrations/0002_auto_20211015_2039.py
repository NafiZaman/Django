# Generated by Django 3.1.2 on 2021-10-15 18:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userupload',
            name='upload_type',
            field=models.CharField(choices=[('profile_pic', 'profile_pic'), ('post', 'post'), ('default', 'default')], default='nothing', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userupload',
            name='user',
            field=models.ForeignKey(default='nothing', on_delete=django.db.models.deletion.CASCADE, to='users.newuser', to_field='email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userupload',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 15, 20, 38, 43, 810325)),
        ),
    ]
