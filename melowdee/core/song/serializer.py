from django.db import transaction
from rest_framework import serializers

from melowdee.core.album.models import Album
from melowdee.core.song.models import Song


class SongSeriaizer(serializers.Serializer):
    name = serializers.CharField(allow_null=False)
    album_id = serializers.CharField(allow_null=False)
    verse_one = serializers.CharField(allow_null=False)
    verse_two = serializers.CharField(allow_null=False)
    verse_three = serializers.CharField(allow_null=True, allow_blank=True)
    verse_four = serializers.CharField(allow_null=True, allow_blank=True)
    chorus = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        album_id = validated_data.get('album_id')
        verse_one = validated_data.get('verse_one')
        verse_two = validated_data.get('verse_two')
        verse_three = validated_data.get('verse_three')
        verse_four = validated_data.get('verse_four')
        chorus = validated_data.get('chorus')

        album_q = Album.objects.filter(id=album_id)
        if album_q.exists():
            album = album_q.first()
            song_q = Song.objects.filter(name=name, album=album_q.first())
            if not song_q.exists():
                with transaction.atomic():
                    song = Song.objects.create(
                        name=name,
                        album=album,
                        verse_one=verse_one,
                        verse_two=verse_two,
                        verse_three=verse_three,
                        verse_four=verse_four,
                        chorus=chorus
                    )
                return song


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'name'
        )


class SongLyricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'verse_one',
            'verse_two',
            'verse_three',
            'verse_four',
            'chorus'
        )





