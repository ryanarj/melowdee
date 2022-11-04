from __future__ import absolute_import, unicode_literals

import asyncio

import arrow
from celery import shared_task
from django.db import transaction

from melowdee.core.wallet.models import Wallet
from melowdee.external.wallet_service import check_balance


@shared_task
def update_balances():
    update_wallets = Wallet.objects.filter(
        updated_at__lte=arrow.utcnow().shift(minutes=-5).datetime
    )

    for wallet in update_wallets:
        check_balance(wallet.address)
        response = asyncio.run(check_balance(wallet.address))
        if response:
            with transaction.atomic():
                response_balance = response.get('balance')
                wallet.balance = response_balance if response_balance else wallet.balance
                wallet.save()
