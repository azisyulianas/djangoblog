# Generated by Django 4.2.3 on 2023-07-27 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_rename_user_userpost_username'),
        ('blog', '0012_alter_blogpostmodel_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentuser', to='users.userpost'),
        ),
    ]
