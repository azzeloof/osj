# Generated by Django 4.0.2 on 2022-02-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0002_alter_image_alt_alter_thing_repo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
