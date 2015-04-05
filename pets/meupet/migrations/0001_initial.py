# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True,
                                        primary_key=True)),
                ('kind', models.TextField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=1, default='M')),
                ('profile_picture', models.ImageField(upload_to='pet_profiles')),
                ('kind', models.ForeignKey(to='meupet.Kind', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
