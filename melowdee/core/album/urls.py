from django.urls import path
from melowdee.core.album import views


urlpatterns = [
    path('add_album/', views.add_album),
    path('all_albums_for_artist/', views.all_albums_for_artist)
]
