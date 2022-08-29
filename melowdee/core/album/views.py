from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from melowdee.core.album.models import Album
from melowdee.core.album.serializers import AddAlbumSerializer, AlbumSerializer
from django.core.cache import cache

@csrf_exempt
def add_album(request):
    """
    add a album
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddAlbumSerializer(data=data)
        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def all_albums_for_artist(request):
    """
    send all artist's albums
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        artist_id = data.get('id')
        album_data = cache.get(f'{artist_id}_artist_data')
        if album_data is None:
            albums = Album.objects.filter(artist_id=artist_id)
            if albums:
                serializer = AlbumSerializer(albums, many=True)
                cache.set(f'{artist_id}_artist_data', serializer.data)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse(data, status=400)
        else:
            return JsonResponse(album_data, safe=False)
