from rest_framework import generics

from api import serializers
from cities.models import City, State
from meupet.models import Pet


class CityList(generics.ListAPIView):
    serializer_class = serializers.CitySerializer

    def get_queryset(self):
        queryset = City.objects.all()
        state = self.request.query_params.get('state', None)
        city = self.request.query_params.get('city', None)
        if state:
            queryset = queryset.filter(state__code=state)
        if city:
            queryset = queryset.filter(search_name__startswith=city)
        return queryset


class ListPets(generics.ListAPIView):
    serializer_class = serializers.PetSerializer

    def get_queryset(self):
        return Pet.objects.select_related('city', 'owner', 'kind').all()


class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer
