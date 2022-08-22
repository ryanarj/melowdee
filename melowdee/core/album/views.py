from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from melowdee.core.album.serializers import AddAlbumSerializer


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
