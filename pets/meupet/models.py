from django.core.urlresolvers import reverse
from django.db import models

from users.models import OwnerProfile


class PetManager(models.Manager):
    def get_lost_or_found(self, kind_id):
        return self.filter(kind__id=kind_id, status__in=[Pet.MISSING, Pet.FOUND])

    def get_for_adoption_adopted(self, kind_id):
        return self.filter(kind__id=kind_id, status__in=[Pet.FOR_ADOPTION, Pet.ADOPTED])

    def get_unpublished_pets(self):
        return self.filter(published=False)


class Kind(models.Model):
    kind = models.TextField(max_length=100)

    def __str__(self):
        return self.kind


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

    class Meta:
        ordering = ['city']


class Pet(models.Model):
    MALE = 'MA'
    FEMALE = 'FE'
    PET_SEX = (
        (FEMALE, 'Fêmea'),
        (MALE, 'Macho',),
    )
    SMALL = 'SM'
    MEDIUM = 'MD'
    LARGE = 'LG'
    PET_SIZE = (
        (SMALL, 'Pequeno'),
        (MEDIUM, 'Médio'),
        (LARGE, 'Grande'),
    )
    MISSING = 'MI'
    FOR_ADOPTION = 'FA'
    ADOPTED = 'AD'
    FOUND = 'FO'
    PET_STATUS = (
        (MISSING, 'Desaparecido'),
        (FOR_ADOPTION, 'Para Adoção'),
        (ADOPTED, 'Adotado'),
        (FOUND, 'Encontrado'),
    )
    owner = models.ForeignKey(OwnerProfile)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    city = models.ForeignKey(City, null=True)
    kind = models.ForeignKey(Kind, null=True)
    status = models.CharField(max_length=2,
                              choices=PET_STATUS,
                              default=MISSING)
    size = models.CharField(max_length=2,
                            choices=PET_SIZE,
                            blank=True)
    sex = models.CharField(max_length=2,
                           choices=PET_SEX,
                           blank=True)
    profile_picture = models.ImageField(upload_to='pet_profiles')
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = PetManager()

    def get_absolute_url(self):
        return reverse('meupet:detail', kwargs={'id': self.id})

    def found_or_adopted(self):
        return self.status == self.ADOPTED or self.status == self.FOUND

    def change_status(self):
        self.status = self.FOUND if self.status == self.MISSING else self.ADOPTED
        self.save()

    def is_found_or_adopted(self):
        return self.status in (self.ADOPTED, self.FOUND)

    def __str__(self):
        return self.name


class Photo(models.Model):
    pet = models.ForeignKey(Pet)
    image = models.ImageField(upload_to='pet_photos')
