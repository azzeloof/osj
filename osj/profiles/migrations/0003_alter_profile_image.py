# Generated by Django 4.0.2 on 2022-02-23 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/profile_photos'),
        ),
    ]