# Generated by Django 4.0.2 on 2022-07-07 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_rename_emailverified_profile_email_verified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='new_email',
        ),
    ]