from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cities", "0003_auto_20170702_2359")]

    operations = [
        migrations.AddField(model_name="city", name="lat", field=models.FloatField(blank=True, null=True)),
        migrations.AddField(model_name="city", name="lon", field=models.FloatField(blank=True, null=True)),
    ]
