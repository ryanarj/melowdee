from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.parsers import JSONParser
from melowdee.auth.user.models import UserMetadata
from melowdee.auth.user.serializers import UserSerializer, UserSigninSerializer
import arrow


@csrf_exempt
@throttle_classes([AnonRateThrottle])
def users(request: WSGIRequest) -> JsonResponse:

    if request.method == 'POST':

        if 'create' in request.path:
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        if 'sign_in' in request.path:
            data = JSONParser().parse(request)
            serializer = UserSigninSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    user_meta = UserMetadata.objects.get(user_id=user.id)
                    data = {
                        'age': user_meta.age,
                        'username': user_meta.user.username,
                    }
                    with transaction.atomic():
                        user_meta.last_login_at = arrow.utcnow().datetime
                        user_meta.save()
                    return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
