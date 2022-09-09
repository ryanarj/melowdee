from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.cache import cache
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.throttling import UserRateThrottle
from melowdee.core.song.models import Song
from melowdee.core.song.serializer import SongSeriaizer, SongSerializer, SongLyricsSerializer


@csrf_exempt
@api_view(['POST', 'GET'])
@throttle_classes([UserRateThrottle])
def songs(request: WSGIRequest) -> JsonResponse:

    if request.method == 'POST':

        if 'create' in request.path:

            data = JSONParser().parse(request)
            serializer = SongSeriaizer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    if request.method == 'GET':

        if 'album_id' in request.path:
            album_id: Optional[str] = request.GET.get('album_id')
            album_data: Optional[dict] = cache.get(f'{album_id}_album_data')
            if album_data is None:
                songs_q: QuerySet[Song] = Song.objects.filter(album_id=album_id)
                if songs_q:
                    song_serializer: SongSerializer = SongSerializer(songs_q, many=True)
                    cache.set(f'{album_id}_album_data', song_serializer.data)
                    return JsonResponse(song_serializer.data, safe=False)
                else:
                    return JsonResponse(album_data, safe=False)
            else:
                return JsonResponse(album_data, safe=False)

        if 'song_id' in request.path:
            song_id: Optional[str] = request.GET.get('album_id')
            song_data: Optional[dict] = cache.get(f'{song_id}_song_data')
            if song_data is None:
                song_q: QuerySet[Song] = Song.objects.filter(id=song_id).first()
                if song_q:
                    song_lyrics_serializer: SongLyricsSerializer = SongLyricsSerializer(song_q)
                    cache.set(f'{song_id}_song_data', song_lyrics_serializer.data)
                    return JsonResponse(song_lyrics_serializer.data, safe=False)
                else:
                    return JsonResponse(song_data, safe=False)
            else:
                return JsonResponse(song_data, safe=False)

        if 'search' in request.path:

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
