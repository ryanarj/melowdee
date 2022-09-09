from django.urls import path
from melowdee.core.artist import views

urlpatterns = [
    path('artists', views.artists),
]
