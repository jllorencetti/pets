# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0013_auto_20150719_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['city']},
        ),
    ]
