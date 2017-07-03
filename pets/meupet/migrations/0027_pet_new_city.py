# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
        ('meupet', '0026_auto_20161211_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='new_city',
            field=models.ForeignKey(null=True, to='cities.City'),
        ),
    ]
