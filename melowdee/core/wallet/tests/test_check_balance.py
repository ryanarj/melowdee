from unittest.mock import patch, AsyncMock

import arrow
from django.contrib.auth.models import User
from django.test import TestCase
from uuid import uuid4

from melowdee.core.wallet.models import Wallet
from melowdee.core.wallet.serializer import BalanceSerializer


class CheckBalance(TestCase):

    @patch('melowdee.core.wallet.serializer.check_balance', new_callable=AsyncMock)
    def test_balance_set_into_cache(self, check_balance_mock):
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        test_hash = str(uuid4())

        expected = {
            'balance': 1.2,
            'address': test_hash,
            'updated_at': arrow.utcnow().datetime
        }

        user = User.objects.create_user(username=test_username, email=test_email)

        Wallet.objects.create(
            public=test_hash, private=test_hash, address=test_hash, user=user
        )
        check_balance_mock.return_value = expected
        actual = BalanceSerializer().set_into_cache(user.id)
        assert actual['balance'] == expected['balance']

    @patch('melowdee.core.wallet.serializer.check_balance', new_callable=AsyncMock)
    def test_balance_get_from_cache(self, check_balance_mock):
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        test_hash = str(uuid4())

        test_response = {
            'balance': 1.2,
            'address': test_hash,
            'updated_at': arrow.utcnow().datetime
        }

        test_response2 = {
            'balance': 1.1,
            'address': test_hash,
            'updated_at': arrow.utcnow().datetime
        }

        user = User.objects.create_user(username=test_username, email=test_email)

        Wallet.objects.create(
            public=test_hash, private=test_hash, address=test_hash, user=user
        )
        check_balance_mock.return_value = test_response
        cache_dict = BalanceSerializer().set_into_cache(user.id)

        cache_dict['updated_at'] = arrow.utcnow().shift(minutes=-5).datetime

        check_balance_mock.return_value = test_response2
        actual = BalanceSerializer().get_from_cache(cache_dict=cache_dict, user_id=user.id)

        assert actual['balance'] == test_response2['balance']
