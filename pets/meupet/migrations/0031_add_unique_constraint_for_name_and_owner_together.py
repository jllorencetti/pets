from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meupet", "0030_auto_20170702_2209"),
    ]

    operations = [migrations.AlterUniqueTogether(name="pet", unique_together=set([("name", "owner")]))]
