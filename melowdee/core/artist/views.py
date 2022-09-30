from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.throttling import UserRateThrottle

from melowdee.core.artist.models import Artist
from melowdee.core.artist.serializers import AddArtistSerializer, AllArtistsSerializer, ArtistSerializer, \
    ArtistNameSerializer
from melowdee.core.song.forms import InputForm
from melowdee.settings import ARTISTS_PER_PAGE
from django.core.cache import cache


class ArtistViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]

    @staticmethod
    def artists(request: WSGIRequest) -> Optional[JsonResponse]:

        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = AddArtistSerializer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        if request.method == 'GET':
            artist_id: Optional[str] = request.GET.get('artist_id')
            if cache.get(artist_id):
                artist_data = cache.get(artist_id)
                return JsonResponse(artist_data, status=200)
            else:
                artist = Artist.objects.filter(id=artist_id).first()
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
                        return JsonResponse(serializer.data, status=200)
                    return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def all_artists(request: WSGIRequest) -> Optional[JsonResponse]:
        if cache.get('all_artist') is None:
            all_arts = Artist.objects.all().order_by('id')
            paginated = Paginator(all_arts, ARTISTS_PER_PAGE)
            page = request.GET.get('page', 1)
            artists = paginated.get_page(page)
            serializer = AllArtistsSerializer(artists, many=True)
            cache.set('all_artist', serializer.data)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            data = cache.get('all_artist')
            return JsonResponse(data, safe=False, status=200)

    @staticmethod
    def artist_by_name(request):
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
