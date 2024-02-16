from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle

from melowdee.core.transaction.models import Transaction, TransactionStatusMap, TransactionStatus
from melowdee.core.transaction.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]

    @method_decorator(csrf_exempt, name='dispatch')
    @staticmethod
    def transactions(request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = TransactionSerializer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    @method_decorator(csrf_exempt, name='dispatch')
    @staticmethod
    def fetch_transactions(request: WSGIRequest, user_id: str) -> Optional[JsonResponse]:

        if request.method == 'GET':
            req_status = request.GET.get('status')

            if req_status not in TransactionStatus.labels:
                req_status = 'pending'

            transaction_q = Transaction.objects.filter(
                user_id=user_id,
                status=req_status
            )

            if transaction_q:
                transactions = []
                for txn in transaction_q:
                    data = {
                        'amount': txn.amount,
                        'created_date': txn.created_at.strftime('%Y-%m-%d'),
                        'id': txn.id,
                        'type': txn.type,
                        'status': txn.status
                    }
                    transactions.append(data)

                return JsonResponse(
                    transactions,
                    safe=False,
                    status=200
                )
