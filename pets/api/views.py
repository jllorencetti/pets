from django.http import HttpResponse, HttpResponseNotAllowed
from rest_framework.renderers import JSONRenderer
from meupet.models import Pet
from api.serializers import PetSerializer


class JsonSerializedResponse(HttpResponse):

    def __init__(self, serilaized_data, **kwargs):
        content = JSONRenderer().render(serilaized_data)
        kwargs['content_type'] = 'application/json'
        super(JsonSerializedResponse, self).__init__(content, **kwargs)


def home(request):
    if (request.method) != 'GET':
        return HttpResponseNotAllowed(['GET'])

    pets = Pet.objects.filter()
    serializer = PetSerializer(pets, many=True, context={'request': request})
    return JsonSerializedResponse(serializer.data)
