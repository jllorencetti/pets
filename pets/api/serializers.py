from rest_framework.fields import ImageField
from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
    StringRelatedField,
)

from cities.models import City, State
from meupet.models import Pet
from users.models import OwnerProfile

city_fields = ("code", "lat", "lon", "name", "search_name")

state_fields = ("abbr", "name")

owner_fields = ("id", "facebook", "name")

pet_fields = (
    "id",
    "city",
    "description",
    "kind",
    "name",
    "owner",
    "profile_picture",
    "thumb_picture",
    "sex",
    "size",
    "status",
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
    name = CharField(source="get_full_name", read_only=True)
    id = HyperlinkedRelatedField(view_name="users:user_profile", read_only=True)

    class Meta:
        model = OwnerProfile
        fields = owner_fields


class PetSerializer(ModelSerializer):
    owner = OwnerSerializer()
    city = CitySerializer()
    kind = StringRelatedField()

    status = CharField(source="status.description", read_only=True)
    sex = CharField(source="get_sex", read_only=True)
    size = CharField(source="get_size", read_only=True)
    thumb_picture = ImageField(read_only=True)

    id = HyperlinkedIdentityField(
        lookup_field="slug", lookup_url_kwarg="pk_or_slug", read_only=True, view_name="meupet:detail"
    )

    class Meta:
        model = Pet
        fields = pet_fields
