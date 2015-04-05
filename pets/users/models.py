from django.db import models
from django.contrib.auth.models import AbstractUser


class OwnerProfile(AbstractUser):
    is_information_confirmed = models.BooleanField(default=False)
    facebook = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.username