from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    HyperlinkedRelatedField,
    StringRelatedField,
)

from cities.models import City, State
from meupet.models import Pet
from users.models import OwnerProfile

city_fields = (
    'code',
    'lat',
    'lon',
    'name',
    'search_name',
)

state_fields = (
    'abbr',
    'name',
)

owner_fields = (
    'id',
    'facebook',
    'name',
)

pet_fields = (
    'id',
    'city',
    'description',
    'kind',
    'name',
    'owner',
    'profile_picture',
    'sex',
    'size',
    'status',
)


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = city_fields


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = state_fields


class OwnerSerializer(ModelSerializer):
    name = CharField(source='get_full_name', read_only=True)
    id = HyperlinkedRelatedField(
        view_name='users:user_profile',
        read_only=True,
    )

    class Meta:
        model = OwnerProfile
        fields = owner_fields


class PetSerializer(ModelSerializer):
    owner = OwnerSerializer()
    city = CitySerializer()
    kind = StringRelatedField()

    status = CharField(source='get_status', read_only=True)
    sex = CharField(source='get_sex', read_only=True)
    size = CharField(source='get_size', read_only=True)

    id = HyperlinkedRelatedField(
        view_name='meupet:detail_by_pk',
        read_only=True
    )

    class Meta:
        model = Pet
        fields = pet_fields
