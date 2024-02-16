from django.db import models
from melowdee.auth.user.models import User


class TransactionType(models.TextChoices):
    PAYMENT = 'payment'
    REFUNDED = 'refunded'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'


class TransactionStatus(models.TextChoices):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class Transaction(models.Model):
    type = models.CharField(max_length=30, default=TransactionType.PAYMENT.value, choices=TransactionType.choices)
    status = models.CharField(max_length=30, default=TransactionStatus.PENDING.value, choices=TransactionStatus.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
