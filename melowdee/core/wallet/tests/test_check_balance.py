from unittest.mock import patch, AsyncMock

import arrow
from django.contrib.auth.models import User
from django.test import TestCase
from uuid import uuid4
from rest_framework.test import APIRequestFactory
from melowdee.core.wallet.models import Wallet
from melowdee.core.wallet.serializer import BalanceSerializer
from melowdee.core.wallet.views import WalletViewSet


class TestCheckBalance(TestCase):

    test_user = None
    test_address = None

    @classmethod
    def setUpClass(cls):

        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        test_hash = str(uuid4())

        test_user = User.objects.create_user(username=test_username, email=test_email)

        Wallet.objects.create(
            public=test_hash, private=test_hash, address=test_hash, user=test_user
        )
        cls.test_user = test_user
        cls.test_address = test_hash

    @classmethod
    def tearDownClass(cls):
        cls.test_user = None
        cls.test_address = None

    @patch('melowdee.core.wallet.serializer.check_balance', new_callable=AsyncMock)
    def test_balance_set_into_cache(self, check_balance_mock):
        expected = {
            'balance': 1.2,
            'address': self.test_address,
            'updated_at': arrow.utcnow().datetime
        }
        check_balance_mock.return_value = expected
        actual = BalanceSerializer().set_into_cache(self.test_user.id)
        assert actual['balance'] == expected['balance']

    @patch('melowdee.core.wallet.serializer.check_balance', new_callable=AsyncMock)
    def test_balance_get_from_cache(self, check_balance_mock):

        test_response = {
            'balance': 1.2,
            'address': self.test_address,
            'updated_at': arrow.utcnow().datetime
        }

        test_response2 = {
            'balance': 1.1,
            'address': self.test_address,
            'updated_at': arrow.utcnow().datetime
        }
        check_balance_mock.return_value = test_response
        cache_dict = BalanceSerializer().set_into_cache(self.test_user.id)

        cache_dict['updated_at'] = arrow.utcnow().shift(minutes=-5).datetime
        check_balance_mock.return_value = test_response2

        actual = BalanceSerializer().get_from_cache(cache_dict=cache_dict, user_id=self.test_user.id)
        assert actual['balance'] == test_response2['balance']

    @patch('melowdee.core.wallet.serializer.check_balance', new_callable=AsyncMock)
    def test_check_balance_endpoint(self, check_balance_mock):
        factory = APIRequestFactory()
        expected = {
            'balance': 1.2,
            'address': self.test_address,
            'updated_at': arrow.utcnow().datetime
        }
        check_balance_mock.return_value = expected
        request = factory.post('/wallets/balance', {
            'user_id': self.test_user.id
        }, format='json')

        response = WalletViewSet().check_balance(request)
        assert str(expected['balance']) in str(response.getvalue())
