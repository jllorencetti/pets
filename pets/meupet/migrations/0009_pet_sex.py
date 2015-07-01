# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0008_auto_20150628_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='sex',
            field=models.CharField(blank=True, choices=[('FE', 'Fêmea'), ('MA', 'Macho')], max_length=2),
            preserve_default=True,
        ),
    ]
