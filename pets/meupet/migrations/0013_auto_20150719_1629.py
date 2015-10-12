# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0012_remove_pet_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='city_fk',
            new_name='city',
        ),
    ]
