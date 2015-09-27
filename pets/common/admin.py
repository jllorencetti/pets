from django.contrib import admin

from . import models


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('fb_share_app_id', 'fb_share_app_secret', 'fb_share_link', 'fb_share_token',)


admin.site.register(models.Configuration, ConfigurationAdmin)
