from django.urls import path
from melowdee.core.song import views


urlpatterns = [
    path('add_song/', views.add_song),
    path('all_songs_for_album/', views.all_songs_for_album),
    path('grab_song_data/', views.grab_song_data)
]
