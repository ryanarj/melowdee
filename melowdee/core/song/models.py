from django.db import models

from melowdee.core.album.models import Album


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    verse_one = models.TextField(null=True, blank=True)
    verse_two = models.TextField(null=True, blank=True)
    verse_three = models.TextField(null=True, blank=True)
    verse_four = models.TextField(null=True, blank=True)
    chorus = models.TextField(null=True, blank=True)
    bridge = models.TextField(null=True, blank=True)


class SongLyrics(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    verse_one = models.TextField(null=True, blank=True)
    verse_two = models.TextField(null=True, blank=True)
    verse_three = models.TextField(null=True, blank=True)
    verse_four = models.TextField(null=True, blank=True)
    chorus = models.TextField(null=True, blank=True)
    bridge = models.TextField(null=True, blank=True)

