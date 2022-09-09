from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from melowdee.auth.user.models import UserMetadata


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=False)
    age = serializers.CharField(required=False, allow_blank=True, max_length=100)
    email = serializers.CharField(allow_null=False)
    password = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        age = validated_data.get('age')
        password = validated_data.get('password')

        if not User.objects.filter(username=username, email=email, password=password).exists():
            with transaction.atomic():
                user = User.objects.create(username=username, email=email, password=password)
                UserMetadata.objects.create(age=age, user=user)
            return user
        else:
            print('User exists')


class UserSigninSerializer(serializers.Serializer):
    email = serializers.CharField(allow_null=False)
    password = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user_q = User.objects.filter(email=email, password=password)
        if user_q.exists():
            user = user_q.first()
            return user
        return None

