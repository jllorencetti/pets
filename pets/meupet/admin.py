from django.contrib import admin

from . import models


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'description', 'status',
                    'published', 'created', 'modified', 'slug')


admin.site.register(models.Pet, PetAdmin)
admin.site.register(models.Kind)
admin.site.register(models.Photo)
admin.site.register(models.City)
