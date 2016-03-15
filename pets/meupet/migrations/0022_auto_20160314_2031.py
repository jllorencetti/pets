# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Pet = apps.get_model('meupet', 'Pet')

    for pet in Pet.objects.all():
        pet.slug = ''
        pet.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0021_auto_20160314_2031'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
