# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0003_auto_20150106_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(
                choices=[('MI', 'Missing'), ('FA', 'For Adoption'), ('AD', 'Adopted'), ('FO', 'Found')], max_length=2,
                default='MI'),
            preserve_default=True,
        ),
    ]
