from django.urls import path
from melowdee.core.article.views import ArticleViewSet


urlpatterns = [
    path('v1/articles', ArticleViewSet().articles)
]
