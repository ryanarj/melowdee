import logging
from django.db import transaction
from rest_framework import serializers

from melowdee.core.transaction.models import Transaction, TransactionStatus, TransactionType

from melowdee.core.wallet.models import Wallet


logger = logging.getLogger('main')


class TransactionSerializer(serializers.Serializer):
    wallet_id = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        wallet_id = validated_data.get('wallet_id')
        wallet_q = Wallet.objects.filter(id=wallet_id)

        if not wallet_q:
            wallet = wallet_q.first()
            user = wallet.user
            balance = wallet.balance

            with transaction.atomic():
                txn = Transaction.objects.create(
                    user=user,
                    status=TransactionStatus.PENDING,
                    type=TransactionType.PAYMENT,
                    amount=balance
                )
                return txn
