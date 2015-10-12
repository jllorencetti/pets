# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0006_pet_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='size',
            field=models.CharField(max_length=2, blank=True, choices=[('SM', 'Pequeno'), ('MD', 'Médio'), ('LG', 'Grande')]),
            preserve_default=True,
        ),
    ]
