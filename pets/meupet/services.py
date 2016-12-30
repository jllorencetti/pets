from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


def send_email(subject, to, template_name, context):
    from_ = settings.DEFAULT_FROM_EMAIL
    body = render_to_string(template_name, context)

    return mail.send_mail(subject, body, from_, [from_, to])


def send_request_action_email(pet):
    subject = _('Update pet registration')
    to = pet.owner.email
    template_name = 'meupet/request_action_email.txt'
    current_site = Site.objects.get_current()

    full_url = 'https://{domain}{path}'.format(
        domain=current_site.domain,
        path=reverse('meupet:update_register', args=[pet.request_key])
    )

    context = {
        'username': pet.owner.first_name,
        'pet': pet.name,
        'days': settings.DAYS_TO_STALE_REGISTER,
        'status': pet.get_status_display().lower(),
        'link': full_url,
        'site_name': current_site.name,
    }

    return send_email(subject, to, template_name, context)
