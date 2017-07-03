# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0029_auto_20170624_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='city',
            field=models.ForeignKey(to='cities.City'),
        ),
    ]
