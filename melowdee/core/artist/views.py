from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from melowdee.core.artist.models import Artist
from melowdee.core.artist.serializer import AddArtistSerializer, AllArtistsSerializer, ArtistSerializer
from melowdee.settings import ARTISTS_PER_PAGE


@csrf_exempt
def add_artist(request):
    """
    add a song
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddArtistSerializer(data=data)
        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def all_artists(request):
    """
    send all artists
    """

    if request.method == 'GET':
        all_arts = Artist.objects.all().order_by('id')
        paginated = Paginator(all_arts, ARTISTS_PER_PAGE)
        page = request.GET.get('page', 1)
        artists = paginated.get_page(page)
        serializer = AllArtistsSerializer(artists, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def grab_artist_data(request):
    """
    get a artists
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArtistSerializer(data=data)
        if serializer and serializer.is_valid():
            artist = serializer.save()
            data = {
                'name': artist.name,
                'about': artist.about,
            }
            return JsonResponse(data, status=201)
        return JsonResponse(serializer.errors, status=400)
