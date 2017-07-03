# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_auto_20170601_2123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['search_name']},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'ordering': ['name']},
        ),
    ]
