from typing import Optional
import logging
import arrow
from django.db import transaction
from rest_framework import serializers

from melowdee.core.wallet.cache_keys import wallet_balance
from melowdee.core.wallet.models import Wallet
from melowdee.auth.user.models import User
import asyncio
from django.core.cache import cache

from melowdee.external.wallet_service import generate_wallet, check_balance


logger = logging.getLogger('main')

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


class BalanceSerializer(serializers.Serializer):
    user_id = serializers.CharField(allow_null=False)

    def create(self, validated_data: dict) -> Optional[dict]:
        logger.info('BalanceSerializer_create')
        user_id = validated_data.get('user_id')
        wallet_bal_cache_dict = cache.get(wallet_balance(user_id=user_id))

        if wallet_bal_cache_dict:
            logger.warning('BalanceSerializer_create_wallet_bal_cache_dict', extra={
                'wallet_bal_cache_dict': wallet_bal_cache_dict
            })
            wallet_bal_cache_dict = self.get_from_cache(cache_dict=wallet_bal_cache_dict, user_id=user_id)
            cache.set(wallet_balance(user_id=user_id), wallet_bal_cache_dict)

        else:
            wallet_bal_cache_dict = self.set_into_cache(user_id=user_id)

        return wallet_bal_cache_dict

    @staticmethod
    def get_from_cache(cache_dict: dict, user_id: str) -> dict:

        if cache_dict:
            updated_at_date = cache_dict['updated_at']

            if updated_at_date < arrow.utcnow().shift(minutes=-1).datetime:
                data = asyncio.run(check_balance(cache_dict['address']))

                if data:
                    logger.warning('BalanceSerializer_get_from_cache', extra={
                        'data': data
                    })
                    wallet = Wallet.objects.filter(user_id=user_id).first()

                    with transaction.atomic():
                        wallet.balance = data.get('balance')
                        wallet.updated_at = arrow.utcnow().datetime
                        wallet.save()

                    cache_dict['balance'] = wallet.balance
                    cache_dict['updated_at'] = wallet.updated_at

                else:
                    logger.error('BalanceSerializer_get_from_cache', extra={
                        'error': 'No Data from response, response_body',
                        'data': data
                    })
        return cache_dict

    @staticmethod
    def set_into_cache(user_id: str) -> dict:

        wallet_bal_dict = {
            'balance': None,
            'address': None,
            'updated_at': None
        }

        wallet_q = Wallet.objects.filter(user_id=user_id)

        if wallet_q:
            wallet = wallet_q.first()
            data = asyncio.run(check_balance(wallet.address))

            with transaction.atomic():
                wallet.balance = data.get('balance')
                wallet.updated_at = arrow.utcnow().datetime
                wallet.save()

            wallet_bal_dict['balance'] = wallet.balance
            wallet_bal_dict['address'] = wallet.address
            wallet_bal_dict['updated_at'] = wallet.updated_at

            cache.set(wallet_balance(user_id=user_id), wallet_bal_dict)

        else:
            print('Need a wallet')

        return wallet_bal_dict
