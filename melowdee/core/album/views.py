from django.core.handlers.wsgi import WSGIRequest
from typing import Optional
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle
from melowdee.core.album.cache_keys import get_artist_id
from melowdee.core.album.models import Album
from melowdee.core.album.serializers import AddAlbumSerializer, AlbumSerializer
from django.core.cache import cache


class AlbumViewSet(viewsets.ViewSet):

    throttle_classes = [UserRateThrottle]

    def albums(self, request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'GET':

            if request.GET.get('artist_id'):
                return self._get_request_artist(request)
            else:
                return JsonResponse(
                    data={'error': 'artist_id not in request'},
                    status=400
                )

        elif request.method == 'POST':
            return self._post_request_albums(request)

    @staticmethod
    def _get_request_artist(request: WSGIRequest) -> JsonResponse:

        artist_id_req = request.GET.get('artist_id').strip()
        artist_id = artist_id_req if artist_id_req is not None and artist_id_req != '' else None

        cache_key = get_artist_id(artist_id)
        album_data = cache.get(cache_key)

        if album_data is None:
            album_q = Album.objects.filter(artist_id=artist_id)
            if album_q:
                album_serializer = AlbumSerializer(album_q, many=True)
                cache.set(cache_key, album_serializer.data)

                return JsonResponse(
                    album_serializer.data,
                    safe=False
                )
            else:
                return JsonResponse(
                    album_data,
                    safe=False,
                    status=200
                )
        else:
            return JsonResponse(
                album_data, safe=False
            )

    @staticmethod
    def _post_request_albums(request: WSGIRequest) -> JsonResponse:
        data = JSONParser().parse(request)
        add_album_serializer = AddAlbumSerializer(data=data)

        if add_album_serializer and add_album_serializer.is_valid():
            add_album_serializer.save()

            return JsonResponse(
                add_album_serializer.data,
                status=201
            )

        return JsonResponse(
            add_album_serializer.errors,
            status=400
        )
