# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0025_auto_20161106_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='request_key',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='pet',
            name='request_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='profile_picture',
            field=models.ImageField(upload_to='pet_profiles', help_text='Maximum image size is 8MB'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='sex',
            field=models.CharField(choices=[('FE', 'Female'), ('MA', 'Male')], blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='pet',
            name='size',
            field=models.CharField(choices=[('SM', 'Small'), ('MD', 'Medium'), ('LG', 'Large')], blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(choices=[('MI', 'Missing'), ('FA', 'For Adoption'), ('AD', 'Adopted'), ('FO', 'Found')], max_length=2, default='MI'),
        ),
    ]
