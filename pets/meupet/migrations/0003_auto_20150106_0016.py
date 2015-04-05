# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0002_auto_20141220_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(default='M', max_length=2,
                                   choices=[('M', 'Missing'), ('F', 'For Adoption'), ('A', 'Adopted'), ('F', 'Found')]),
            preserve_default=True,
        ),
    ]
