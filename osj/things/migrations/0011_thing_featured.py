# Generated by Django 4.0.2 on 2022-02-24 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0010_alter_thing_description_alter_thing_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
