# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0016_auto_20160105_2019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pet',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='pet',
            name='profile_picture',
            field=models.ImageField(upload_to='pet_profiles', help_text='Tamanho máximo da imagem é 2MB'),
        ),
    ]
