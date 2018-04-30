import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone, crypto
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from meupet import services
from users.models import OwnerProfile


class PetQuerySet(models.QuerySet):
    def _filter_by_kind(self, kind):
        try:
            return self.actives().filter(kind__id=int(kind)).select_related('city')
        except ValueError:
            return self.actives().filter(kind__slug=kind).select_related('city')

    def get_unpublished_pets(self):
        return self.filter(published=False)

    def get_staled_pets(self):
        """
        Pets considered as staled are not modified after a given
        number of days and don't have a request_sent date
        """
        stale_date = timezone.now() - timezone.timedelta(days=settings.DAYS_TO_STALE_REGISTER)
        return self.filter(
            modified__lt=stale_date,
            request_sent__isnull=True,
            status__in=PetStatus.objects.filter(final=False)
        )

    def actives(self):
        """
        Return only pets with active = True
        """
        return self.filter(active=True)

    def get_expired_pets(self):
        """Expired pets have request_sent date older than expected"""
        expire_date = timezone.now() - timezone.timedelta(days=settings.DAYS_TO_STALE_REGISTER)
        return self.filter(active=True, request_sent__lt=expire_date)


class KindManager(models.Manager):
    def count_pets(self, status):
        return self.filter(pet__status__in=status, pet__active=True) \
            .annotate(num_pets=models.Count('pet')).order_by('kind')


class Kind(models.Model):
    kind = models.TextField(max_length=100, unique=True)
    slug = AutoSlugField(max_length=30, populate_from='kind')

    objects = KindManager()

    def __str__(self):
        return self.kind


def get_slug(instance):
    city = ''
    if instance.city:
        city = instance.city.name
    return slugify('{}-{}'.format(instance.name, city))


class StatusGroup(models.Model):
    slug = AutoSlugField(max_length=64, unique=True, populate_from='name')
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class PetStatus(models.Model):
    group = models.ForeignKey(StatusGroup, related_name='statuses', blank=True, null=True)
    code = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=64)
    next_status = models.OneToOneField('self', blank=True, null=True)
    final = models.BooleanField(default=False)

    class Meta:
        ordering = ('description',)

    def __str__(self):
        return self.description

    @property
    def next(self):
        return self.next_status


class Pet(TimeStampedModel):
    MALE = 'MA'
    FEMALE = 'FE'
    PET_SEX = (
        (FEMALE, _('Female')),
        (MALE, _('Male')),
    )
    SMALL = 'SM'
    MEDIUM = 'MD'
    LARGE = 'LG'
    PET_SIZE = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (LARGE, _('Large')),
    )
    owner = models.ForeignKey(OwnerProfile)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    city = models.ForeignKey('cities.City')
    kind = models.ForeignKey(Kind, null=True)
    status = models.ForeignKey(PetStatus, related_name='pets', blank=True, null=True)
    size = models.CharField(max_length=2,
                            choices=PET_SIZE,
                            blank=True)
    sex = models.CharField(max_length=2,
                           choices=PET_SEX,
                           blank=True)
    profile_picture = models.ImageField(upload_to='pet_profiles',
                                        help_text=_('Maximum image size is 8MB'))
    published = models.BooleanField(default=False)  # published on facebook
    request_sent = models.DateTimeField(null=True, blank=True)
    request_key = models.CharField(blank=True, max_length=40)
    active = models.BooleanField(default=True)
    slug = AutoSlugField(max_length=50, populate_from=get_slug, unique=True)

    objects = PetQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('meupet:detail', kwargs={'pk_or_slug': self.slug})

    def change_status(self):
        self.status = self.status.next
        self.save()

    def is_found_or_adopted(self):
        return self.status.final

    def get_status(self):
        return self.status.description

    def get_sex(self):
        return dict(self.PET_SEX).get(self.sex)

    def get_size(self):
        return dict(self.PET_SIZE).get(self.size)

    def request_action(self):
        hash_input = (crypto.get_random_string(5) + self.name).encode('utf-8')
        self.request_key = hashlib.sha1(hash_input).hexdigest()

        if not services.send_request_action_email(self):
            return

        self.request_sent = timezone.now()
        self.save(update_modified=False)

    def activate(self):
        self.request_sent = None
        self.request_key = ''
        self.active = True
        self.save()

    def deactivate(self):
        if not services.send_deactivate_email(self):
            return

        self.active = False
        self.save(update_modified=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        unique_together = ('name', 'owner')


class Photo(models.Model):
    pet = models.ForeignKey(Pet)
    image = models.ImageField(upload_to='pet_photos')
