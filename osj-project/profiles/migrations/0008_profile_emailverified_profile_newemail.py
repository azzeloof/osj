# Generated by Django 4.0.2 on 2022-07-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='emailVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='newEmail',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
