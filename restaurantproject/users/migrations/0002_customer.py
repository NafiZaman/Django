# Generated by Django 3.1.2 on 2021-09-20 12:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('newuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.newuser')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('address', models.CharField(max_length=50)),
                ('post_code', models.IntegerField()),
                ('phone', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('users.newuser',),
        ),
    ]
