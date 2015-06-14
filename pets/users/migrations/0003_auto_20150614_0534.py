# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_ownerprofile_is_information_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerprofile',
            name='facebook',
            field=models.CharField(blank=True, null=True, validators=[users.validators.validate_facebook_url], max_length=250),
            preserve_default=True,
        ),
    ]
