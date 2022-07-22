from django.contrib.auth.models import User
from django.db import models


class UserMetadata(models.Model):
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

