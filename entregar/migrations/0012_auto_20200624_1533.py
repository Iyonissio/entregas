# Generated by Django 3.0.7 on 2020-06-24 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entregar', '0011_auto_20200624_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='celular',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='nome',
        ),
    ]
