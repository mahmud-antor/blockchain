# Generated by Django 2.2.3 on 2019-07-17 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Self',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.IntegerField(default=7919)),
                ('private_key', models.IntegerField(default=7927)),
                ('df_key', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]