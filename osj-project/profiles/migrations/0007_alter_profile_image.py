# Generated by Django 4.0.2 on 2022-04-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_photos'),
        ),
    ]