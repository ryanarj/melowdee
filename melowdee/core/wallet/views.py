from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle

from melowdee.core.artist.models import Artist
from melowdee.core.wallet.serializer import WalletSerializer, BalanceSerializer
from django.core.cache import cache
from melowdee.core.wallet.models import Wallet


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

        if request.method == 'GET':
            artist_id = request.GET.get('artist_id')
            wallet = Wallet.objects.filter(artist_id=artist_id).first()
            if wallet:
                data = {'wallet': wallet}
                return JsonResponse(
                    data,
                    safe=False,
                    status=200
                )

            else:
                with transaction.atomic():
                    artist_id = Artist.objects.filter(artist_id=artist_id).first()

                    wallet = Wallet.objects.create(
                        user=user, artist=artist
                    )
                    return wallet
                return JsonResponse(
                    data={},
                    safe=False,
                    status=404
                )

    @method_decorator(csrf_exempt, name='dispatch')
    @staticmethod
    def check_balance(request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = BalanceSerializer(data=data)
            if serializer and serializer.is_valid():
                wallet = serializer.save()
                data = {'balance': wallet.get('balance')}
                return JsonResponse(data, status=201)
            return JsonResponse(serializer.errors, status=400)
