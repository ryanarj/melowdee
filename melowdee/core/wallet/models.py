from django.db import models
from melowdee.auth.user.models import User


class Wallet(models.Model):

    public = models.CharField(max_length=200)
    private = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

