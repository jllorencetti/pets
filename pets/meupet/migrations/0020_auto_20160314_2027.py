# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Pet = apps.get_model('meupet', 'Pet')

    for index, pet in enumerate(Pet.objects.filter(slug='')):
        pet.slug = index
        pet.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0019_pet_slug'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
