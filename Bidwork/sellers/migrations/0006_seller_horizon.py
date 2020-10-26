# Generated by Django 3.1.2 on 2020-10-25 06:36

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0005_seller_remainedhour'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='horizon',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5),
        ),
    ]