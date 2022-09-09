from django.core.handlers.wsgi import WSGIRequest
from typing import Optional
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle
from melowdee.core.album.models import Album
from melowdee.core.album.serializers import AddAlbumSerializer, AlbumSerializer
from django.core.cache import cache


@csrf_exempt
@throttle_classes([UserRateThrottle])
def albums(request: WSGIRequest) -> JsonResponse:
    """
    send all artist's albums
    """
    if request.method == 'GET':

        if request.GET.get('artist_id'):
            artist_id: Optional[str] = request.GET.get('artist_id').strip()
            artist_id: Optional[str] = artist_id if artist_id is not None and artist_id != '' else None
            album_data: dict = cache.get(f'{artist_id}_artist_data')

            if album_data is None:
                album_q = Album.objects.filter(artist_id=artist_id)
                if album_q:
                    album_serializer: AlbumSerializer = AlbumSerializer(album_q, many=True)
                    cache.set(f'{artist_id}_artist_data', album_serializer.data)
                    return JsonResponse(album_serializer.data, safe=False)
                else:
                    return JsonResponse(album_data, safe=False)
            else:
                return JsonResponse(album_data, safe=False)

    if request.method == 'POST':

        if 'create' in request.path:
            data: dict = JSONParser().parse(request)
            add_album_serializer: AddAlbumSerializer = AddAlbumSerializer(data=data)
            if add_album_serializer and add_album_serializer.is_valid():
                add_album_serializer.save()
                return JsonResponse(add_album_serializer.data, status=201)
            return JsonResponse(add_album_serializer.errors, status=400)
