# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
                ('search_name', models.CharField(db_index=True, max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('abbr', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='cities.State'),
        ),
    ]
