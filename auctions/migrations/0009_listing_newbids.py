# Generated by Django 3.1 on 2021-10-06 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20211001_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='newBids',
            field=models.FloatField(default=0.0, max_length=10),
        ),
    ]
