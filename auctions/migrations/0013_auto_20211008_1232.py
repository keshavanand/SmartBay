# Generated by Django 3.1 on 2021-10-08 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(related_name='listingWatchlisting', to='auctions.Listing'),
        ),
    ]
