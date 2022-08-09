


from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from melowdee.core.artist.serializer import AddArtistSerializer


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
