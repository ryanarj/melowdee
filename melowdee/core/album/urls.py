from django.urls import path
from melowdee.core.album import views


urlpatterns = [
    path('add_album/', views.add_album),
    path('get_albums_for_artist', views.get_albums_for_artist)
]
