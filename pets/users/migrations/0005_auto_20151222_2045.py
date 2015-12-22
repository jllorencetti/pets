# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150815_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerprofile',
            name='facebook',
            field=models.URLField(null=True, validators=[users.validators.validate_facebook_url], max_length=250, blank=True),
        ),
    ]
