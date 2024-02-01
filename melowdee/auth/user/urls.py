from django.urls import path
from melowdee.auth.user.views import UserViewSet


urlpatterns = [
    path('v1/users/', UserViewSet().users),
    path('v1/users/sign_in/', UserViewSet().user_sign_in),
]
