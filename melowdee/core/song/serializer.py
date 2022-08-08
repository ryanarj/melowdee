from django.db import transaction
from rest_framework import serializers

from melowdee.core.album.models import Album
from melowdee.core.artist.models import Artist
from melowdee.core.song.models import Song


class SongSeriaizer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)
    album = serializers.CharField(allow_null=False)
    artist = serializers.CharField(allow_null=False)
    verse_one = serializers.CharField(allow_null=False)
    verse_two = serializers.CharField(allow_null=False)
    verse_three = serializers.CharField(allow_null=True)
    verse_four = serializers.CharField(allow_null=True)
    chorus = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        album = validated_data.get('album')
        artist = validated_data.get('artist')
        verse_one = validated_data.get('verse_one')
        verse_two = validated_data.get('verse_two')
        verse_three = validated_data.get('verse_three')
        verse_four = validated_data.get('verse_four')
        chorus = validated_data.get('chorus')

        album_q = Album.objects.filter(name=album, artist__name=artist)
        if not album_q.exists():
            artist_obj = Artist.objects.filter(name=artist)

            if not artist_obj.exists():
                with transaction.atomic():
                    artist_obj = Artist.objects.create(name=artist)
                    album_obj = Album.objects.create(name=album, artist=artist)
            else:
                artist_obj = Artist.objects.create(name=artist)

        song_q = Song.objects.filter(name=name, album=album_q.first())
        if not song_q.exists():
            song = Song.objects.create(name=name, album=album_obj)







