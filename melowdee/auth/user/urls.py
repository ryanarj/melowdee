from django.urls import path
from melowdee.auth.user import views


urlpatterns = [
    path('user_signup/', views.user_signup),
    path('user_sign_in/', views.user_sign_in)
]