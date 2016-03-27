from django.contrib import admin
from django.core.management import call_command

from . import models


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'description', 'status',
                    'published', 'created', 'modified', 'slug')
    actions = ['request_unsolvedcases_status']

    def request_unsolvedcases_status(self, request, queryset):
        call_command('request_unsolvedcases_status', queryset=queryset)

    request_unsolvedcases_status.short_description = 'Pedir atualização de status'

admin.site.register(models.Pet, PetAdmin)
admin.site.register(models.Kind)
admin.site.register(models.Photo)
admin.site.register(models.City)
