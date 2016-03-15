# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import meupet.models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0020_auto_20160314_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False, populate_from=meupet.models.get_slug),
        ),
    ]
