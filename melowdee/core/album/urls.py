from django.urls import path
from melowdee.core.album import views


urlpatterns = [
    path('albums', views.albums),
]
