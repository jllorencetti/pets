# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_kinds(apps, schema_editor):
    Kind = apps.get_model("meupet", "Kind")
    Kind.objects.create(kind="Gato")
    Kind.objects.create(kind="Cachorro")
    Kind.objects.create(kind="Aves")


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_kinds)
    ]
