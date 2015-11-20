from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from meupet import models


def get_adoption_kinds():
    return get_kind_list([models.Pet.FOR_ADOPTION, models.Pet.ADOPTED])


def get_lost_kinds():
    return get_kind_list([models.Pet.MISSING, models.Pet.FOUND])


def get_kind_list(status):
    return models.Kind.objects.filter(pet__status__in=status).annotate(num_pets=Count('pet')).order_by('kind')


class MeuPetEspecieMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MeuPetEspecieMixin, self).get_context_data(**kwargs)
        context['kind_lost'] = get_lost_kinds()
        context['kind_adoption'] = get_adoption_kinds()
        return context


class AboutPageView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/about.html'


class AssociacoesView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/associacoes.html'


def not_found(request):
    return render(request, 'staticpages/404.html')


def home(request):
    pets = models.Pet.objects.select_related('city').order_by('-id')[:6]
    return render(request, 'common/home.html', {'pets': pets})
