from django.urls import path
from melowdee.core.wallet.views import WalletViewSet


urlpatterns = [
    path('wallets', WalletViewSet().wallets),
    path('wallets/balance', WalletViewSet().check_balance)
]
