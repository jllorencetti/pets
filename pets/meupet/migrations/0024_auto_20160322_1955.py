# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_slugs(apps, schema_editor):
    kind_model = apps.get_model('meupet', 'Kind')

    for kind in kind_model.objects.all():
        kind.slug = ''
        kind.save()


def dummy_rollback(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0023_auto_20160322_1955'),
    ]

    operations = [
        migrations.RunPython(update_slugs, dummy_rollback)
    ]
