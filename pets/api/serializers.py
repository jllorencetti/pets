from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    HyperlinkedRelatedField,
    StringRelatedField,
)

from cities.models import City, State
from meupet.models import Pet
from users.models import OwnerProfile


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'search_name',)


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'abbr',)


class OwnerSerializer(ModelSerializer):
    name = CharField(source='get_full_name', read_only=True)
    id = HyperlinkedRelatedField(
        view_name='users:user_profile',
        read_only=True,
    )

    class Meta:
        model = OwnerProfile
        fields = ('name', 'id', 'facebook',)


class PetSerializer(ModelSerializer):
    owner = OwnerSerializer()
    city = StringRelatedField()
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
        fields = ('id', 'owner', 'name', 'description', 'city', 'kind', 'status',
                  'size', 'sex', 'profile_picture',)
