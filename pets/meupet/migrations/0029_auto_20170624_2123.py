# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0028_auto_20170421_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='new_city',
        ),
        migrations.AlterField(
            model_name='pet',
            name='city',
            field=models.ForeignKey(null=True, to='cities.City'),
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
