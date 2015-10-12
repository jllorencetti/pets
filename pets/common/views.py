from django.shortcuts import render
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView

from meupet import models


def get_kind_list():
    return models.Kind.objects.all().order_by('kind')


class MeuPetEspecieMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(MeuPetEspecieMixin, self).get_context_data(**kwargs)
        context['kind_lost'] = get_kind_list()
        context['kind_adoption'] = get_kind_list()
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
