from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle

from melowdee.core.article.serializers import CreateArticleSerializer


@csrf_exempt
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def articles(request: WSGIRequest) -> JsonResponse:

    if request.method == 'POST':

        if 'create' in request.path:
            data: dict = JSONParser().parse(request)
            serializer: CreateArticleSerializer = CreateArticleSerializer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
