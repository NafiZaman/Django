# Generated by Django 3.1.2 on 2021-10-23 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_remove_usersetting_personal_info_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='upload_visibility',
            field=models.CharField(choices=[('public', 'public'), ('friends', 'friends'), ('private', 'private')], default='friends', max_length=50),
        ),
    ]
