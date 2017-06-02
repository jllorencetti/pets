from rest_framework import generics

from api import serializers
from cities.models import State
from meupet.models import Pet


class ListPets(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = serializers.PetSerializer


class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer
