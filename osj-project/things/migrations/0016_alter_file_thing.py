# Generated by Django 4.0.2 on 2022-06-13 19:35

from django.db import migrations, models
import django.db.models.deletion
import things.models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0015_alter_file_thing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_set', to='things.thing', validators=[things.models.validateNumberOfFiles]),
        ),
    ]
