from django.contrib import admin

from meupet import models


class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'kind',
        'city',
        'description',
        'status',
        'created',
        'modified',
        'published',
        'request_sent',
        'active',
    )
    list_filter = (
        'status',
        'kind',
        'created',
        'active',
    )


admin.site.register(models.Pet, PetAdmin)
admin.site.register(models.Kind)
admin.site.register(models.Photo)
