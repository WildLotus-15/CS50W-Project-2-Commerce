# Generated by Django 3.2.5 on 2021-07-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
