from django.urls import path
from melowdee.core.article import views


urlpatterns = [
    path('articles', views.articles)
]
