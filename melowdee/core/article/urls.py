from django.urls import path
from melowdee.core.article import views


urlpatterns = [
    path('add_article/', views.add_article)
]
