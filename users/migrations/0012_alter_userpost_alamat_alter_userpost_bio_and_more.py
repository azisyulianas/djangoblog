# Generated by Django 4.2.3 on 2023-07-27 12:40

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_rename_user_userpost_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='alamat',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='full_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.content_file_name),
        ),
    ]
