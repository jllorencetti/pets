from django import template
from django.template.loader import render_to_string

from meupet.models import Kind

register = template.Library()


@register.simple_tag()
def sidemenu():
    return render_to_string('meupet/_sidemenu.html', {
        'kind_lost': Kind.objects.lost_kinds(),
        'kind_adoption': Kind.objects.adoption_kinds(),
    })
