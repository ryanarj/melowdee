# Generated by Django 4.0.6 on 2022-08-08 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
