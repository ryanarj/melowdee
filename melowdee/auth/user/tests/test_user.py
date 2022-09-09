from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from melowdee.auth.user.views import users


class UserTestCase(TestCase):

    def test_user_signup(self):
        factory = APIRequestFactory()
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        request = factory.post('/users/create/', {
            'username': test_username,
            'email': test_email,
            'age': 1,
            'password': 'test'
        }, format='json')
        response = users(request)

        user = User.objects.filter(username=test_username, email=test_email)
        assert user.exists() is True
        assert response.status_code == 201

    def test_user_sign_in(self):
        factory = APIRequestFactory()
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'

        request = factory.post('/user/create_user/', {
            'username': test_username,
            'email': test_email,
            'age': 1,
            'password': 'test'
        }, format='json')
        users(request)

        request = factory.post('/user/sign_in/', {
            'email': test_email,
            'password': 'test'
        }, format='json')
        response = users(request)
        assert response.status_code == 201
