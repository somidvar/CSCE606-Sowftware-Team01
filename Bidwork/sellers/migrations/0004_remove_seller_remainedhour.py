# Generated by Django 3.1.2 on 2020-10-25 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_seller_remainedhour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='remainedHour',
        ),
    ]