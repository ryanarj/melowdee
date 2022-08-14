from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from melowdee.auth.user.views import user_signup


class UserTestCase(TestCase):

    def test_user_signup(self):
        factory = APIRequestFactory()
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        request = factory.post('/user_signup/', {
            'username': test_username,
            'email': test_email,
            'age': 1,
            'password': 'test'
        }, format='json')
        user_signup(request)

        user = User.objects.filter(username=test_username, email=test_email)
        assert user.exists() is True
