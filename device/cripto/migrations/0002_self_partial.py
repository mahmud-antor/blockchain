# Generated by Django 2.2.3 on 2019-07-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cripto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='self',
            name='partial',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]