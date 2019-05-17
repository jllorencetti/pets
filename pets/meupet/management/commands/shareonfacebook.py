import facebook

from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Configuration
from meupet.models import Pet


class Command(BaseCommand):
    """
    This command is not pretty at all, using the database for
    these configurations is not the the best approach, but it
    makes easier to update the values for the configuration
    """

    leave_locale_alone = True

    def __init__(self):
        self.config = Configuration.objects.first()
        super(Command, self).__init__()

    @staticmethod
    def get_message(pet):
        return "{0}: {1}, {2}".format(pet.status.description, pet.name, pet.city)

    def handle(self, *args, **options):
        api = facebook.GraphAPI(
            access_token=self.config.fb_share_token, version=settings.FACEBOOK_SHARE_GRAPH_API_VERSION
        )
        url = self.config.fb_share_link

        for pet in Pet.objects.get_unpublished_pets():
            api.put_object(
                parent_object="me",
                connection_name="feed",
                message=self.get_message(pet),
                link=url.format(pet.get_absolute_url()),
            )

            pet.published = True
            pet.save()
