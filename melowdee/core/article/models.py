from django.db import models

from melowdee.auth.user.models import User
from melowdee.core.artist.models import Artist
from melowdee.core.album.models import Album
from melowdee.core.song.models import Song


class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Song, blank=True, null=True, on_delete=models.SET_NULL)
