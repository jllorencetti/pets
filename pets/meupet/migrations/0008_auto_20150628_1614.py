# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0007_pet_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(default='MI', max_length=2, choices=[('MI', 'Desaparecido'), ('FA', 'Para Adoção'), ('AD', 'Adotado'), ('FO', 'Encontrado')]),
            preserve_default=True,
        ),
    ]
