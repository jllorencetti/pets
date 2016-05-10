from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from meupet import models


class MeuPetEspecieMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(MeuPetEspecieMixin, self).get_context_data(**kwargs)
        context['kind_lost'] = models.Kind.objects.lost_kinds()
        context['kind_adoption'] = models.Kind.objects.adoption_kinds()
        return context


class AboutPageView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/about.html'


class AssociacoesView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/associacoes.html'


def not_found(request):
    return render(request, 'staticpages/404.html')


def home(request):
    return render(request, 'common/home.html')
