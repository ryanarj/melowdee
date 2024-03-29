from typing import Optional

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle

from melowdee.core.album.cache_keys import get_all_artist
from melowdee.core.artist.cache_keys import get_artist_data
from melowdee.core.artist.models import Artist
from melowdee.core.artist.serializers import AddArtistSerializer, AllArtistsSerializer, ArtistSerializer
from melowdee.core.song.forms import InputForm
from melowdee.settings import ARTISTS_PER_PAGE
from django.core.cache import cache


class ArtistViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]

    @csrf_exempt
    def artists(self, request: WSGIRequest) -> Optional[JsonResponse]:
        if request.method == 'POST':
            return self._post_artists(request)

    @csrf_exempt
    def get_artist_by_id(self, request: WSGIRequest, artist_id: str) -> Optional[JsonResponse]:
        if request.method == 'GET':
            if artist_id:
                return self._get_request_artist(artist_id)

    @staticmethod
    def all_artists(request: WSGIRequest) -> Optional[JsonResponse]:
        all_artist_cache = cache.get(get_all_artist())

        if all_artist_cache is None:
            all_arts = Artist.objects.all().order_by('id')
            paginated = Paginator(all_arts, ARTISTS_PER_PAGE)

            page = request.GET.get('page', 1)
            artists = paginated.get_page(page)
            serializer = AllArtistsSerializer(artists, many=True)
            cache.set(get_all_artist(), serializer.data)

            return JsonResponse(
                serializer.data,
                safe=False,
                status=200
            )

        else:
            return JsonResponse(
                all_artist_cache,
                safe=False,
                status=200
            )

    @staticmethod
    def artist_by_name(request: WSGIRequest) -> Optional[HttpResponse]:
        form = InputForm(request.POST)
        if form.is_valid():
            artist = Artist.objects.filter(name=form.cleaned_data['artist_name']).first()
            if artist:
                return render(
                    request,
                    'result.html',
                    {'form': form, 'artist_name': artist.name})
            else:
                return render(
                    request,
                    'index.html',
                    {'artist_name': form.cleaned_data['artist_name']}
                )

    @staticmethod
    def _get_request_artist(artist_id: str) -> Optional[JsonResponse]:
        if cache.get(get_artist_data(artist_id)):
            artist_data = cache.get(artist_id)
            return JsonResponse(
                artist_data,
                status=200
            )

        else:
            artist = Artist.objects.filter(id=artist_id).first()
            if not artist:
                print('NOT FOUND')
            if artist:
                serializer = ArtistSerializer(
                    data={
                        'name': artist.name,
                        'id': artist.id,
                        'about': artist.about
                    }
                )

                if serializer and serializer.is_valid():
                    cache.set(artist_id, serializer.data)

                    return JsonResponse(
                        serializer.data,
                        status=200
                    )
            return JsonResponse(
                data={},
                status=404
            )

    @staticmethod
    def _post_artists(request: WSGIRequest) -> JsonResponse:
        data = JSONParser().parse(request)
        serializer = AddArtistSerializer(data=data)

        if serializer and serializer.is_valid():
            serializer.save()

            return JsonResponse(
                serializer.data,
                status=201
            )

        return JsonResponse(
            serializer.errors,
            status=400
        )
