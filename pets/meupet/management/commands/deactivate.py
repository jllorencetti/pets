from django.core.management import BaseCommand

from meupet.models import Pet


class Command(BaseCommand):
    """
    Deactivates every expired pets
    """
    leave_locale_alone = True

    def handle(self, *args, **options):
        for pet in Pet.objects.get_expired_pets():
            pet.deactivate()
