# Generated by Django 4.0.2 on 2022-02-20 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thing',
            name='tags',
        ),
    ]
