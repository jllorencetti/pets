# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0022_auto_20160314_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='kind',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=30, populate_from='kind', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kind',
            name='kind',
            field=models.TextField(max_length=100, unique=True),
        ),
    ]
