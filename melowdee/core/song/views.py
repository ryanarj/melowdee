from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.cache import cache

from melowdee.core.song.models import Song
from melowdee.core.song.serializer import SongSeriaizer, SongSerializer, SongLyricsSerializer


@csrf_exempt
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
def song_search(request):
    """
    search song
    """
    if request.method == 'GET':
        search_value = request.GET.get('search')
        if search_value is not None:
            song = Song.objects.filter(name__icontains=search_value).first()
            if song:
                serializer = SongSerializer(song, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({}, safe=False)
        else:
            return JsonResponse({}, safe=False)
