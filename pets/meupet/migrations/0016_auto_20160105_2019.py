# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0015_pet_published'),
    ]

    operations = [
        migrations.AddField(
                model_name='pet',
                name='created',
                field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 20, 19, 6, 548541, tzinfo=utc),
                                           auto_now_add=True),
                preserve_default=False,
        ),
        migrations.AddField(
                model_name='pet',
                name='modified',
                field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 20, 19, 15, 300296, tzinfo=utc),
                                           auto_now=True),
                preserve_default=False,
        ),
    ]
