from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.cache import cache
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.throttling import UserRateThrottle
from melowdee.core.song.models import Song
from melowdee.core.song.serializer import SongSeriaizer, SongSerializer, SongLyricsSerializer


@csrf_exempt
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def add_song(request):
    """
    add a song
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSeriaizer(data=data)
        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def all_songs_for_album(request):
    """
    send all artist's albums
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        album_id = data.get('id')
        album_data = cache.get(f'{album_id}_album_data')
        if album_data is None:
            songs = Song.objects.filter(album_id=album_id)
            if songs:
                serializer = SongSerializer(songs, many=True)
                cache.set(f'{album_id}_album_data', serializer.data)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse(album_data, safe=False)
        else:
            return JsonResponse(album_data, safe=False)


@csrf_exempt
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def grab_song_data(request):
    """
    send all artist's albums
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        song_id = data.get('id')
        song_data = cache.get(f'{song_id}_song_data')
        if song_data is None:
            song = Song.objects.filter(id=song_id).first()
            if song:
                serializer = SongLyricsSerializer(song)
                cache.set(f'{song_id}_song_data', serializer.data)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse(song_data, safe=False)
        else:
            return JsonResponse(song_data, safe=False)

@csrf_exempt
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def song_search(request):
    """
    search song
    """
    if request.method == 'GET':
        search_value = request.GET.get('search').strip()
        search_value = search_value if search_value is not None and search_value != '' else None
        if search_value:
            songs = Song.objects.filter(name__icontains=search_value)
            if songs:
                serializer = SongSerializer(songs, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({}, safe=False)
        else:
            return JsonResponse({}, safe=False)
