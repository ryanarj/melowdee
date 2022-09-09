from django.urls import path
from melowdee.auth.user import views


urlpatterns = [
    path('users', views.users),
]
