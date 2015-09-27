# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fb_share_token', models.TextField(max_length=250)),
                ('fb_share_app_id', models.TextField(max_length=20)),
                ('fb_share_app_secret', models.TextField(max_length=35)),
                ('fb_share_link', models.TextField(max_length=50)),
            ],
        ),
    ]
