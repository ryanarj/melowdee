from django.urls import path
from melowdee.user import views


urlpatterns = [
    path('user_signup/', views.user_signup)
]
