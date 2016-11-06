# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0024_auto_20160322_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
