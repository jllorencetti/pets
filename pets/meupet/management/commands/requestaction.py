from django.core.management.base import BaseCommand

from meupet.models import Pet


class Command(BaseCommand):
    leave_locale_alone = True
    
    def handle(self, *args, **options):
        for pet in Pet.objects.get_staled_pets():
            pet.request_action()
