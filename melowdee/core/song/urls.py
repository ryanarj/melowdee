from django.urls import path
from melowdee.core.song import views


urlpatterns = [
    path('songs', views.songs)
]
