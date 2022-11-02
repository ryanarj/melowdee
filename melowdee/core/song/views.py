from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle

from melowdee.core.song.cache_keys import get_song_data, get_song_album_data
from melowdee.core.song.forms import InputForm, URLForm
from melowdee.core.song.models import Song
from melowdee.core.song.serializer import SongSerializer, NewSongSerializer, SongLyricsSerializer


class SongViewSet(viewsets.ModelViewSet):

    throttle_classes = [UserRateThrottle]

    def songs(self, request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            return self._post_song(request)

        elif request.method == 'GET':
            return self._get_song(request)

    @staticmethod
    def song_search(request: WSGIRequest) -> Optional[JsonResponse]:

        search_value = request.GET.get('search').strip() if request.GET.get('search') else None
        clean_search_value = search_value if search_value is not None and search_value != '' else None

        if clean_search_value:
            songs_q = Song.objects.filter(
                name__icontains=clean_search_value
            )

            if songs_q:
                serializer = SongSerializer(songs_q, many=True)

                return JsonResponse(
                    data=serializer.data,
                    safe=False
                )

            else:
                return JsonResponse(
                    data={},
                    safe=False
                )

        else:
            return JsonResponse(
                data={}, safe=False
            )

    @staticmethod
    def from_album(request: WSGIRequest) -> Optional[JsonResponse]:

        album_id = request.GET.get('album_id')
        cache_key = get_song_album_data(album_id)
        album_song_data = cache.get(cache_key)

        if album_song_data is None:
            song_q = Song.objects.filter(album=album_id)
            if song_q:
                song_serializer = NewSongSerializer(song_q, many=True)
                cache.set(cache_key, song_serializer.data)

                return JsonResponse(
                    data=song_serializer.data,
                    safe=False
                )
            else:
                return JsonResponse(
                    data={'error': 'Songs for album found'},
                    safe=False,
                    status=404
                )
        else:
            return JsonResponse(
                data=album_song_data,
                safe=False
            )

    @staticmethod
    def index(request: WSGIRequest):
        context = {}
        context['form1'] = InputForm()
        context['form2'] = URLForm()
        return render(request, "index.html", context)

    @staticmethod
    def _get_song(request: WSGIRequest) -> JsonResponse:
        song_id = request.GET.get('song_id')
        cache_key = get_song_data(song_id)
        song_data = cache.get(cache_key)

        if song_data is None:
            song_q: QuerySet[Song] = Song.objects.filter(id=song_id).first()
            if song_q:
                song_lyrics_serializer = SongLyricsSerializer(song_q)
                cache.set(cache_key, song_lyrics_serializer.data)

                return JsonResponse(
                    data=song_lyrics_serializer.data,
                    safe=False
                )

            else:
                return JsonResponse(
                    data={'error': 'Song Not found'},
                    safe=False,
                    status=404
                )

        else:
            return JsonResponse(
                data=song_data,
                safe=False
            )

    @staticmethod
    def _post_song(request: WSGIRequest) -> JsonResponse:
        data = JSONParser().parse(request)
        serializer = NewSongSerializer(data=data)

        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(
                data=serializer.data,
                status=201
            )

        return JsonResponse(
            data=serializer.errors,
            status=400
        )
