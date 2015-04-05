from django.views.generic.base import ContextMixin

from meupet import models


def get_kind_list():
    return models.Kind.objects.all()


class MeuPetEspecieMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(MeuPetEspecieMixin, self).get_context_data(**kwargs)
        context['kind_lost'] = get_kind_list()
        context['kind_adoption'] = get_kind_list()
        return context
