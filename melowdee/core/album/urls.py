from django.urls import path
from melowdee.core.album.views import AlbumViewSet


urlpatterns = [
    path('v1/albums', AlbumViewSet().albums),
]
