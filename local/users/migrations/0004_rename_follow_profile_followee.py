# Generated by Django 4.2.3 on 2023-07-13 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_profile_followees_remove_profile_followings_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follow',
            new_name='followee',
        ),
    ]