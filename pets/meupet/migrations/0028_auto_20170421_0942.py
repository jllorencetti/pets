# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from common import utils


def migrate_cities(apps, scheme_editor):
    """Updates the city based on the new model"""
    Pet = apps.get_model('meupet', 'Pet')
    City = apps.get_model('cities', 'City')

    for pet in Pet.objects.all():
        if pet.city:
            city = City.objects.filter(search_name=utils.clear_text(pet.city.city).lower()).first()
            if city:
                pet.new_city = city
                pet.save()


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0027_pet_new_city'),
    ]

    operations = [
        migrations.RunPython(migrate_cities),
    ]
