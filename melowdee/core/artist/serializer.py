from melowdee.core.artist.models import Artist
from django.db import transaction
from rest_framework import serializers


class AddArtistSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)
    about = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        name = validated_data.get('name')
        about = validated_data.get('about')

        if not Artist.objects.filter(name=name).exists():
            with transaction.atomic():
                artist = Artist.objects.create(name=name, about=about)
            return artist
        else:
            print('Artist exists')


class AllArtistsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = (
            'id',
            'name'
        )


class ArtistSerializer(serializers.Serializer):
    id = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        id = validated_data.get('id')
        artist = Artist.objects.filter(id=id)
        if artist.exists():
            return artist.first()
        else:
            print('Artist exists')
