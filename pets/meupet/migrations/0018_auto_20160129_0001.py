# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0017_auto_20160116_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='profile_picture',
            field=models.ImageField(upload_to='pet_profiles', help_text='Tamanho máximo da imagem é 8MB'),
        ),
    ]
