from django.urls import path
from melowdee.core.wallet.views import WalletViewSet


urlpatterns = [
    path('v1/wallets', WalletViewSet().wallets),
    path('v1/wallets/balance', WalletViewSet().check_balance)
]
