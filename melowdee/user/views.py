from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from melowdee.user.models import UserMetadata
from melowdee.user.serializers import UserSerializer, UserSigninSerializer


@csrf_exempt
def user_signup(request):
    """
    sign up a user
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_sign_in(request):
    """
    sign in a user
    """
    import arrow
    if request.method == 'POST':
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
                user_meta.last_login_at = arrow.utcnow().datetime
                user_meta.save()
                return JsonResponse(data, status=201)
        return JsonResponse(serializer.errors, status=400)
