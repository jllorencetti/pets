# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150614_0534'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ownerprofile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='email',
            field=models.EmailField(blank=True, verbose_name='email address', max_length=254),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', verbose_name='groups', to='auth.Group', related_name='user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='last_login',
            field=models.DateTimeField(null=True, blank=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='username',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', unique=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30),
        ),
    ]
