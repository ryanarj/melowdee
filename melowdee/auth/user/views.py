from typing import Dict, Optional

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.parsers import JSONParser
from melowdee.auth.user.models import UserMetadata
from melowdee.auth.user.serializers import CreateUserSerializer, UserSigninSerializer
import arrow


@csrf_exempt
@throttle_classes([AnonRateThrottle])
def users(request: WSGIRequest) -> JsonResponse:

    if request.method == 'POST':

        if 'create' in request.path:
            data: Dict[str, str] = JSONParser().parse(request)
            user_serializer: CreateUserSerializer = CreateUserSerializer(data=data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data, status=201)
            return JsonResponse(user_serializer.errors, status=400)

        if 'sign_in' in request.path:
            data: Dict[str, str] = JSONParser().parse(request)
            user_sign_in_serializer: UserSigninSerializer = UserSigninSerializer(data=data)
            if user_sign_in_serializer.is_valid():
                user: Optional[User] = user_sign_in_serializer.save()
                if user:
                    user_meta: UserMetadata = UserMetadata.objects.get(user_id=user)
                    data = {
                        'age': user_meta.age,
                        'username': user_meta.user.username,
                    }
                    with transaction.atomic():
                        user_meta.last_login_at = arrow.utcnow().datetime
                        user_meta.save()
                    return JsonResponse(data, status=201)
            return JsonResponse(user_sign_in_serializer.errors, status=400)
