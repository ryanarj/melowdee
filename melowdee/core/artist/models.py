from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)
