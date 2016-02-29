# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20151222_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownerprofile',
            name='phone',
            field=models.CharField(verbose_name='Telefone', blank=True, max_length=30),
        ),
    ]
