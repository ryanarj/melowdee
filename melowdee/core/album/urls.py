from django.urls import path
from melowdee.core.album.views import AlbumViewSet


urlpatterns = [
    path('albums', AlbumViewSet().albums),
]
