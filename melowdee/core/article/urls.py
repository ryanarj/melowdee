from django.urls import path
from melowdee.core.article.views import ArticleViewSet


urlpatterns = [
    path('articles', ArticleViewSet().articles)
]
