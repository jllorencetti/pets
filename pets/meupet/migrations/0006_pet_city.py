# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0005_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='city',
            field=models.CharField(max_length=50, default='Araras'),
            preserve_default=False,
        ),
    ]
