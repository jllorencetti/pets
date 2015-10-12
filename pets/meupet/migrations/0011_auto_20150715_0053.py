# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_city(apps, schema_editor):
    Pet = apps.get_model('meupet', 'Pet')
    City = apps.get_model('meupet', 'City')
    for pet in Pet.objects.all():
        city, created = City.objects.get_or_create(city=pet.city.title())
        pet.city_fk = city
        pet.save()


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0010_auto_20150715_0050'),
    ]

    operations = [
        migrations.RunPython(set_city)
    ]
