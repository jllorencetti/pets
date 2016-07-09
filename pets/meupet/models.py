from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

from users.models import OwnerProfile

from autoslug import AutoSlugField


class PetManager(models.Manager):
    def _filter_by_kind(self, kind):
        try:
            return self.filter(kind__id=int(kind)).select_related('city')
        except ValueError:
            return self.filter(kind__slug=kind).select_related('city')

    def get_lost_or_found(self, kind):
        return self._filter_by_kind(kind).filter(status__in=[Pet.MISSING, Pet.FOUND])

    def get_for_adoption_adopted(self, kind):
        return self._filter_by_kind(kind).filter(status__in=[Pet.FOR_ADOPTION, Pet.ADOPTED])

    def get_unpublished_pets(self):
        return self.filter(published=False)


class KindManager(models.Manager):
    def count_pets(self, status):
        return self.filter(pet__status__in=status).annotate(num_pets=models.Count('pet')).order_by('kind')

    def lost_kinds(self):
        return self.count_pets([Pet.MISSING, Pet.FOUND])

    def adoption_kinds(self):
        return self.count_pets([Pet.FOR_ADOPTION, Pet.ADOPTED])


class Kind(models.Model):
    kind = models.TextField(max_length=100, unique=True)
    slug = AutoSlugField(max_length=30, populate_from='kind')

    objects = KindManager()

    def __str__(self):
        return self.kind


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

    class Meta:
        ordering = ['city']


def get_slug(instance):
    city = ''
    if instance.city:
        city = instance.city.city
    return slugify('{}-{}'.format(instance.name, city))


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
    profile_picture = models.ImageField(upload_to='pet_profiles',
                                        help_text='Tamanho máximo da imagem é 8MB')
    published = models.BooleanField(default=False)  # published on facebook
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(max_length=50,
                         populate_from=get_slug,
                         unique=True)

    objects = PetManager()


    def get_absolute_url(self):
        return reverse('meupet:detail', kwargs={'pk_or_slug': self.slug})

    def found_or_adopted(self):
        return self.status == self.ADOPTED or self.status == self.FOUND

    def change_status(self):
        self.status = self.FOUND if self.status == self.MISSING else self.ADOPTED
        self.save()

    def is_found_or_adopted(self):
        return self.status in (self.ADOPTED, self.FOUND)

    def get_status(self):
        return dict(self.PET_STATUS).get(self.status)

    def get_sex(self):
        return dict(self.PET_SEX).get(self.sex)

    def get_size(self):
        return dict(self.PET_SIZE).get(self.size)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Photo(models.Model):
    pet = models.ForeignKey(Pet)
    image = models.ImageField(upload_to='pet_photos')
