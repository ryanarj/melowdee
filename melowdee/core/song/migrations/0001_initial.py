# Generated by Django 4.0.6 on 2022-08-06 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('album', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.album')),
            ],
        ),
        migrations.CreateModel(
            name='SongLyrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse_one', models.TextField(blank=True, null=True)),
                ('verse_two', models.TextField(blank=True, null=True)),
                ('verse_three', models.TextField(blank=True, null=True)),
                ('verse_four', models.TextField(blank=True, null=True)),
                ('chorus', models.TextField(blank=True, null=True)),
                ('bridge', models.TextField(blank=True, null=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.song')),
            ],
        ),
    ]