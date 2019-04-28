from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from users.validators import validate_facebook_url


class OwnerProfile(AbstractUser):
    is_information_confirmed = models.BooleanField(default=False)
    facebook = models.URLField(max_length=250, blank=True, null=True,
                               validators=[validate_facebook_url])
    phone = models.CharField('Telefone', max_length=30, blank=True)

    def get_absolute_url(self):
        return reverse('users:user_profile', args=[self.id])

    def __str__(self):
        return self.username
