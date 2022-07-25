from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from melowdee.user.serializers import UserSerializer

@csrf_exempt
def user_signup(request):
    """
    Create
    """

    if request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
