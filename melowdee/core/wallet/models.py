from django.db import models
from melowdee.auth.user.models import User
from melowdee.core.artist.models import Artist


class Wallet(models.Model):

    public = models.CharField(max_length=200, null=True, blank=True)
    private = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

