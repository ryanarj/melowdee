from django.urls import path
from melowdee.core.artist import views


urlpatterns = [
    path('add_artist/', views.add_artist)
]
