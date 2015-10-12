# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0014_auto_20150802_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
