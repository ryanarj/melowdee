from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from melowdee.core.song.serializer import SongSeriaizer


@csrf_exempt
def add_song(request):
    """
    add a song
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSeriaizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

