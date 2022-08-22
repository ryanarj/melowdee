from melowdee.core.album.models import Album
from django.db import transaction
from rest_framework import serializers

from melowdee.core.artist.models import Artist


class AddAlbumSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)
    about = serializers.CharField(required=False, allow_blank=True, max_length=100)
    artist_id = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        about = validated_data.get('about')
        artist_id = validated_data.get('artist_id')

        if not Album.objects.filter(name=name, artist_id=artist_id).exists():
            artist = Artist.objects.filter(id=artist_id)

            if not artist:
                with transaction.atomic():
                    album = Album.objects.create(name=name, about=about, artist=artist.first())

                return album
            else:
                print('Artist does not exists')
        else:
            print('Album exists')
