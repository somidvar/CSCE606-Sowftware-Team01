# Generated by Django 3.1.2 on 2020-11-13 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0008_buyers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Buyers',
        ),
    ]