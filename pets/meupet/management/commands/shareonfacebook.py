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

    def get_token(self):
        return self.config.fb_share_token

    def get_attachment(self, pet):
        link = self.config.fb_share_link
        attachment = {
            'link': link.format(pet.get_absolute_url()),
        }
        return attachment

    def handle(self, *args, **options):
        api = facebook.GraphAPI(self.get_token())

        for pet in Pet.objects.get_unpublished_pets():
            msg = '{}: {}, {}'.format(pet.get_status_display(), pet.name, pet.city)

            api.put_wall_post(msg, attachment=self.get_attachment(pet))

            pet.published = True
            pet.save()
