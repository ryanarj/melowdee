from django.urls import path
from melowdee.core.artist.views import ArtistViewSet

urlpatterns = [
    path('v1/artists/', ArtistViewSet().artists),
    path('v1/artists/<artist_id>', ArtistViewSet().get_artist_by_id),
    path('v1/artists/all/', ArtistViewSet().all_artists),
]

