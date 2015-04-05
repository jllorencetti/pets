# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0004_auto_20150122_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('image', models.ImageField(upload_to='pet_photos')),
                ('pet', models.ForeignKey(to='meupet.Pet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
