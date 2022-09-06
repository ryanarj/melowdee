
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from melowdee.core.article.serializers import AddArticleSerializer

@csrf_exempt
def add_article(request):
    """
    add a album
    """

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddArticleSerializer(data=data)
        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
