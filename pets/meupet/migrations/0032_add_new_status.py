from autoslug import AutoSlugField

import django.db.models.deletion
from django.db import migrations, models

status_group = (
    {
        'slug': 'para-adocao',
        'name': 'Para Adoção',
        'statuses': {
            'status': {'code': 'ado', 'description': 'Para Adoção', 'final': False},
            'next': {'code': 'ado_next', 'description': 'Adotado', 'final': True},
        },
    },
    {
        'slug': 'desaparecidos',
        'name': 'Desaparecidos',
        'statuses': {
            'status': {'code': 'desa', 'description': 'Desaparecido', 'final': False},
            'next': {'code': 'desa_next', 'description': 'Encontrado', 'final': True},
        },
    },
    {
        'slug': 'achados',
        'name': 'Achados',
        'statuses': {
            'status': {'code': 'acha', 'description': 'Achado', 'final': False},
            'next': {'code': 'acha_next', 'description': 'Encontrado', 'final': True},
        },
    },
)


def migrate(apps, schema_editor):
    StatusGroup = apps.get_model('meupet', 'StatusGroup')
    PetStatus = apps.get_model('meupet', 'PetStatus')
    Pet = apps.get_model('meupet', 'Pet')

    for group in status_group:
        statuses = group.pop('statuses')
        new_group = StatusGroup.objects.create(**group)

        st = new_group.statuses.create(**statuses['status'])
        st_next = new_group.statuses.create(**statuses['next'])
        st.next_status = st_next
        st.save()

    Pet.objects.filter(status='MI').update(new_status=PetStatus.objects.get(code='desa'))
    Pet.objects.filter(status='FO').update(new_status=PetStatus.objects.get(code='desa_next'))
    Pet.objects.filter(status='FA').update(new_status=PetStatus.objects.get(code='ado'))
    Pet.objects.filter(status='AD').update(new_status=PetStatus.objects.get(code='ado_next'))


def rollback(apps, schema_editor):
    PetStatus = apps.get_model('meupet', 'PetStatus')
    Pet = apps.get_model('meupet', 'Pet')

    Pet.objects.filter(new_status=PetStatus.objects.get(code='desa')).update(status='MI')
    Pet.objects.filter(new_status=PetStatus.objects.get(code='desa_next')).update(status='FO')
    Pet.objects.filter(new_status=PetStatus.objects.get(code='ado')).update(status='FA')
    Pet.objects.filter(new_status=PetStatus.objects.get(code='ado_next')).update(status='AD')


class Migration(migrations.Migration):
    dependencies = [
        ('meupet', '0031_add_unique_constraint_for_name_and_owner_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', AutoSlugField(editable=False, max_length=64, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PetStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='statuses', to='meupet.StatusGroup')),
                ('description', models.CharField(max_length=64)),
                ('final', models.BooleanField(default=False)),
                ('next_status', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                     to='meupet.PetStatus')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='new_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='pets', to='meupet.PetStatus'),
        ),
        migrations.AlterModelOptions(
            name='petstatus',
            options={'ordering': ('description',)},
        ),
        migrations.RunPython(migrate, rollback),
    ]
