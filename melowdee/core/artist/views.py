from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from melowdee.core.artist.models import Artist
from melowdee.core.artist.serializers import AddArtistSerializer, AllArtistsSerializer, ArtistSerializer
from melowdee.settings import ARTISTS_PER_PAGE
from django.core.cache import cache


@csrf_exempt
def artists(request):
    """
    add a song
    """

    if request.method == 'POST':
        if 'add' in request.path:
            data = JSONParser().parse(request)
            serializer = AddArtistSerializer(data=data)
            if serializer and serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

    if request.method == 'GET':

        if 'artist_id' in request.path:

            data = JSONParser().parse(request)
            if cache.get(data.get('id')):
                artist_data = cache.get(data.get('id'))
                return JsonResponse(artist_data, status=201)
            else:
                serializer = ArtistSerializer(data=data)
                if serializer and serializer.is_valid():
                    artist = serializer.save()
                    data = {
                        'name': artist.name,
                        'about': artist.about,
                    }
                    cache.set(artist.id, data)
                    return JsonResponse(data, status=201)
                return JsonResponse(serializer.errors, status=400)
        else:

            if cache.get('all_artist') is None:
                all_arts = Artist.objects.all().order_by('id')
                paginated = Paginator(all_arts, ARTISTS_PER_PAGE)
                page = request.GET.get('page', 1)
                artists = paginated.get_page(page)
                serializer = AllArtistsSerializer(artists, many=True)
                cache.set('all_artist', serializer.data)
                return JsonResponse(serializer.data, safe=False)
            else:
                data = cache.get('all_artist')
                return JsonResponse(data, safe=False)
