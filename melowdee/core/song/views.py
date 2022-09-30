from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle

from melowdee.core.song.forms import InputForm, URLForm
from melowdee.core.song.models import Song
from melowdee.core.song.serializer import SongSeriaizer, SongSerializer, SongLyricsSerializer


class SongViewSet(viewsets.ModelViewSet):

    throttle_classes = [UserRateThrottle]

    @staticmethod
    def songs(request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = SongSeriaizer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        if request.method == 'GET':
            song_id: Optional[str] = request.GET.get('song_id')
            song_data: Optional[dict] = cache.get(f'{song_id}_song_data')
            if song_data is None:
                song_q: QuerySet[Song] = Song.objects.filter(id=song_id).first()
                if song_q:
                    song_lyrics_serializer: SongLyricsSerializer = SongLyricsSerializer(song_q)
                    cache.set(f'{song_id}_song_data', song_lyrics_serializer.data)
                    return JsonResponse(song_lyrics_serializer.data, safe=False)
                else:
                    return JsonResponse(data={'error': 'Song Not found'}, safe=False, status=404)
            else:
                return JsonResponse(song_data, safe=False)

    @staticmethod
    def song_search(request: WSGIRequest) -> Optional[JsonResponse]:

        search_value: Optional[str] = request.GET.get('search').strip() \
            if request.GET.get('search') else None

        clean_search_value: Optional[str] = search_value \
            if search_value is not None and search_value != '' else None

        if clean_search_value:
            songs: QuerySet[Optional[Song]] = Song.objects.filter(name__icontains=clean_search_value)
            if songs:
                serializer = SongSerializer(songs, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({}, safe=False)
        else:
            return JsonResponse({}, safe=False)

    @staticmethod
    def from_album(request: WSGIRequest) -> Optional[JsonResponse]:

        album_id: Optional[str] = request.GET.get('album_id')
        album_song_data: Optional[dict] = cache.get(f'{album_id}_song_data')
        if album_song_data is None:
            song_q: QuerySet[Song] = Song.objects.filter(album=album_id)
            if song_q:
                song_serializer: SongSerializer = SongSerializer(song_q, many=True)
                cache.set(f'{album_id}_song_data', song_serializer.data)
                return JsonResponse(song_serializer.data, safe=False)
            else:
                return JsonResponse(data={'error': 'Songs for album found'}, safe=False, status=404)
        else:
            return JsonResponse(album_song_data, safe=False)

    @staticmethod
    def index(request: WSGIRequest):
        context = {}
        context['form1'] = InputForm()
        context['form2'] = URLForm()
        return render(request, "index.html", context)
