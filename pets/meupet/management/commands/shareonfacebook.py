from django.core.management.base import BaseCommand

import facebook

from common.models import Configuration
from meupet.models import Pet


class Command(BaseCommand):
    """
    This command is not pretty at all, using the database for
    these configurations is not the the best approach, but it
    makes easier to update the values for the configuration
    """

    def __init__(self):
        self.config = Configuration.objects.first()
        super(Command, self).__init__()

    def get_renewed_token(self):
        """
        As the long lived token is valid for 60 days only,
        I choose to store the configuration on the database
        and always renew it when the command is executed.
        """
        api = facebook.GraphAPI(self.config.fb_share_token)
        long_token = api.extend_access_token(
            self.config.fb_share_app_id,
            self.config.fb_share_app_secret
        )
        self.config.fb_share_token = long_token['access_token']
        self.config.save()
        return self.config.fb_share_token

    def get_attachment(self, pet):
        link = self.config.fb_share_link
        attachment = {
            'link': link.format(pet.get_absolute_url()),
        }
        return attachment

    def handle(self, *args, **options):
        api = facebook.GraphAPI(self.get_renewed_token())

        for pet in Pet.objects.get_unpublished_pets():
            msg = '{}: {}, {}'.format(pet.get_status_display(), pet.name, pet.city)

            api.put_wall_post(msg, attachment=self.get_attachment(pet))

            pet.published = True
            pet.save()
