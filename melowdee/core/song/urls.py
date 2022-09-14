from django.urls import path
from melowdee.core.song.views import SongViewSet


urlpatterns = [
    path('songs', SongViewSet().songs),
    path('songs/search', SongViewSet().song_search),
    path('songs/from_album', SongViewSet().from_album)
]
