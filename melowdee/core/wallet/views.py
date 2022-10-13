from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle
from melowdee.core.wallet.serializer import WalletSerializer

class WalletViewSet(viewsets.ModelViewSet):

    throttle_classes = [UserRateThrottle]

    @method_decorator(csrf_exempt, name='dispatch')
    @staticmethod
    def wallets(request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = WalletSerializer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
