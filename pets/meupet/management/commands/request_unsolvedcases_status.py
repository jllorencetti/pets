from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from common.models import Configuration
from django.template.loader import render_to_string
from meupet.models import Pet


class Command(BaseCommand):
    """
    This command will send e-mail to users requesting for case status
    """

    def __init__(self):
        self.config = Configuration.objects.first()
        super(Command, self).__init__()

    def handle(self, *args, **options):
        unsolved_cases = Pet.objects.get_unsolved_cases()

        for pet in unsolved_cases:
            send_mail(
                subject='Atualização de Status do Seu Pet',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pet.owner.email],
                message=render_to_string('meupet/request_unsolvedcases_status.txt', {'pet': pet})
            )
