import requests

from django.core.management import BaseCommand

from common.models import Configuration


class Command(BaseCommand):
    leave_locale_alone = True
    base_url = "https://graph.facebook.com/oauth/access_token"

    def handle(self, *args, **options):
        configuration = Configuration.objects.first()

        token = self.refresh_token(configuration)

        configuration.fb_share_token = token
        configuration.save()

    def refresh_token(self, configuration):
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": configuration.fb_share_app_id,
            "client_secret": configuration.fb_share_app_secret,
            "fb_exchange_token": configuration.fb_share_token,
        }

        resp = requests.get(self.base_url, params=params)
        resp.raise_for_status()

        return resp.json()["access_token"]
