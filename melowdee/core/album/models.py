from django.db import models

from melowdee.core.artist.models import Artist


class Album(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
