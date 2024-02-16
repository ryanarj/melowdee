from django.urls import path

from melowdee.core.transaction.views import TransactionViewSet


urlpatterns = [
    path('v1/transactions', TransactionViewSet().transactions),
    path('v1/transactions/<user_id>/$', TransactionViewSet().fetch_transactions)
]
