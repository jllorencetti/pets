from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meupet', '0032_add_new_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='status',
        ),
    ]
