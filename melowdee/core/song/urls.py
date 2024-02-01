from django.urls import path
from melowdee.core.song.views import SongViewSet


urlpatterns = [
    path('v1/songs', SongViewSet().songs),
    path('v1/songs/search', SongViewSet().song_search),
    path('v1/songs/from_album', SongViewSet().from_album),
    path('v1/index', SongViewSet().index)
]
