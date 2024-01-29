# Generated by Django 4.2.9 on 2024-01-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_wallet_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='private',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='public',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
