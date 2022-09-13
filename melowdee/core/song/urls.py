from django.urls import path
from melowdee.core.song.views import SongViewSet


urlpatterns = [
    path('songs', SongViewSet().songs),
    path('song_search', SongViewSet().song_search)
]
