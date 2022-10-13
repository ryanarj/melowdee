from django.db import transaction
from rest_framework import serializers
from melowdee.core.wallet.models import Wallet
from melowdee.auth.user.models import User
import asyncio

from melowdee.external.wallet_service import generate_wallet


class WalletSerializer(serializers.Serializer):
    user_id = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        user_id = validated_data.get('user_id')

        wallet_q = Wallet.objects.filter(user_id=user_id)

        if not wallet_q:

            user = User.objects.filter(id=user_id).first()
            data = asyncio.run(generate_wallet(user.password))

            with transaction.atomic():
                wallet = Wallet.objects.create(
                    user=user, public=data.get('public'), private=data.get('private'), address=data.get('address')
                )
                return wallet
