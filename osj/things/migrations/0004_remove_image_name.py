# Generated by Django 3.2.9 on 2022-02-10 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0003_alter_file_name_alter_image_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
    ]
