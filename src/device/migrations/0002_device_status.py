# Generated by Django 2.0.9 on 2019-07-23 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
