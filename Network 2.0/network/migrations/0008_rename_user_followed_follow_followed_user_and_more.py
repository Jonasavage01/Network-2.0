# Generated by Django 5.0.2 on 2024-04-22 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_user_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='user_followed',
            new_name='followed_user',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='user',
            new_name='follower',
        ),
    ]
