# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0011_auto_20150715_0053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='city',
        ),
    ]
