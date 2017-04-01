from rest_framework import generics

from api.serializers import PetSerializer
from meupet.models import Pet


class ListPets(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
