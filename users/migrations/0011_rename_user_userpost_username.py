# Generated by Django 4.2.3 on 2023-07-27 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_username_userpost_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpost',
            old_name='user',
            new_name='username',
        ),
    ]
