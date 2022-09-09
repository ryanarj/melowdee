from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle
from melowdee.core.album.models import Album
from melowdee.core.album.serializers import AddAlbumSerializer, AlbumSerializer
from django.core.cache import cache

@csrf_exempt
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
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
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def get_albums_for_artist(request):
    """
    send all artist's albums
    """
    if request.method == 'GET':
        artist_id = request.GET.get('artist_id').strip()
        artist_id = artist_id if artist_id is not None and artist_id != '' else None
        album_data = cache.get(f'{artist_id}_artist_data')
        if album_data is None:
            albums = Album.objects.filter(artist_id=artist_id)
            if albums:
                serializer = AlbumSerializer(albums, many=True)
                cache.set(f'{artist_id}_artist_data', serializer.data)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse(album_data, safe=False)
        else:
            return JsonResponse(album_data, safe=False)
