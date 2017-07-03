from django.contrib import admin

from cities import models

admin.site.register(models.State)
admin.site.register(models.City)
