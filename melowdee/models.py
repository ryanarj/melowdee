from django.contrib.auth.models import User
from django.db import models


class UserMetadata(models.Model):
    user_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.CharField(max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

