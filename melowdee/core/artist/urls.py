from django.urls import path
from melowdee.core.artist.views import ArtistViewSet

urlpatterns = [
    path('artists/', ArtistViewSet().artists),
    path('artists/artist_by_user_id/', ArtistViewSet().get_artist_by_user_id),
    path('artists/all/', ArtistViewSet().all_artists),
    path('artists/artist_by_name', ArtistViewSet().artist_by_name)
]

