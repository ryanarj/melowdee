from django.contrib.auth.models import User

from melowdee.core.artist.models import Artist
from django.db import transaction
from rest_framework import serializers


class AddArtistSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)
    about = serializers.CharField(required=False, allow_blank=True, max_length=100)
    user_id = serializers.CharField(allow_blank=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        about = validated_data.get('about')
        user_id = validated_data.get('user_id')
        print('test')
        if not Artist.objects.filter(name=name).exists():
            print(f'user_id_{user_id}')
            user = User.objects.get(id=user_id)
            with transaction.atomic():
                artist = Artist.objects.create(name=name, about=about, user=user)
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


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class ArtistNameSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        artist = Artist.objects.filter(name=name)
        if artist.exist():
            return artist.first()
        else:
            print('Artist does not exists')