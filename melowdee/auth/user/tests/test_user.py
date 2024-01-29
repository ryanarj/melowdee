from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from melowdee.auth.user.views import UserViewSet


class UserTestCase(TestCase):

    def test_user_signup(self):
        factory = APIRequestFactory()
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'
        request = factory.post('/users/', {
            'username': test_username,
            'email': test_email,
            'age': 1,
            'password': 'test'
        }, format='json')
        response = UserViewSet().users(request)
        user = User.objects.filter(username=test_username, email=test_email)
        self.assertTrue(user.exists())
        self.assertEqual(response.status_code, 201)

    def test_user_sign_in(self):
        factory = APIRequestFactory()
        test_username = 'Test23'
        test_email = 'Test23@melowdee.com'

        request = factory.post('/users/', {
            'username': test_username,
            'email': test_email,
            'age': 1,
            'password': 'test'
        }, format='json')
        UserViewSet().users(request)

        request = factory.post('/users/sign_in/', {
            'email': test_email,
            'password': 'test'
        }, format='json')
        response = UserViewSet().user_sign_in(request)
        self.assertEqual(response.status_code, 200)
