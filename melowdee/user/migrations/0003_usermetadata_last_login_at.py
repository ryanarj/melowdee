# Generated by Django 4.0.6 on 2022-07-27 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_user_id_usermetadata_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermetadata',
            name='last_login_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
