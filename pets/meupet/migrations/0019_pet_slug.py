# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import meupet.models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0018_auto_20160129_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, blank=True, populate_from=meupet.models.get_slug),
        ),
    ]
