# Generated by Django 4.2.3 on 2023-07-27 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_userpost_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpost',
            old_name='username',
            new_name='user',
        ),
    ]