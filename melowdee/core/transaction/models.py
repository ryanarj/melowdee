from django.db import models
from melowdee.auth.user.models import User


class TransactionType(models.IntegerChoices):
    PAYMENT = 0, 'payment'
    REFUNDED = 1, 'refunded'
    WITHDRAWAL = 2, 'withdrawal'
    TRANSFER = 3, 'transfer'


class TransactionStatus(models.IntegerChoices):
    PENDING = 0, 'pending'
    COMPLETED = 1, 'completed'
    FAILED = 2, 'failed'


class Transaction(models.Model):
    type = models.IntegerField(default=TransactionType.PAYMENT, choices=TransactionType.choices)
    status = models.IntegerField(default=TransactionStatus.PENDING, choices=TransactionStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
