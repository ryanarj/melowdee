from django.db import transaction
from rest_framework import serializers

from melowdee.core.article.models import Article
from melowdee.core.artist.models import Artist


class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=False)
    description = serializers.CharField(allow_null=False)
    artist_id = serializers.CharField(allow_null=False)

    def create(self, validated_data: dict):
        title = validated_data.get('title')
        description = validated_data.get('description')
        artist_id = validated_data.get('artist_id')

        artist = Artist.objects.filter(id=artist_id)

        with transaction.atomic():
            article = Article.objects.create(
                title=title,
                description=description,
                artist=artist.first() if artist else None
            )
        return article
