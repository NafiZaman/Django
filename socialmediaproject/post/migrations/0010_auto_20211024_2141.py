# Generated by Django 3.1.2 on 2021-10-24 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20211024_2138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_date_time',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_image',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='comment_text',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='comment_date_time',
            new_name='date_added',
        ),
    ]
