from django.urls import path
from melowdee.auth.user.views import UserViewSet


urlpatterns = [
    path('users/', UserViewSet().users),
    path('users/sign_in/', UserViewSet().user_sign_in),
]
