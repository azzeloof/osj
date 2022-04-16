# Generated by Django 4.0.2 on 2022-02-24 17:42

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=django_bleach.models.BleachField(blank=True, max_length=1000),
        ),
    ]