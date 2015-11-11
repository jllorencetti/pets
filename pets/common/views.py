from functools import reduce

from django.shortcuts import render
from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView

from meupet import models


def get_kind_list():
    return models.Kind.objects.all().order_by('kind')


class MeuPetEspecieMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(MeuPetEspecieMixin, self).get_context_data(**kwargs)
        kinds = models.Kind.objects.all()

        status_list = [("kind_lost", models.Pet.MISSING),
                       ("kind_adoption", models.Pet.FOR_ADOPTION)]

        kind_list = models.Kind.objects.all()

        pets = [(status_name, kind,
                 models.Pet.objects.get_by_kind_and_status(kind, status))
                for kind in kind_list
                for status_name, status in status_list]

        pets = [(status, kind, p.count())
                for status, kind, p in pets
                if not p is None]

        print(pets)

        def _reduce(agg, elem):
            status, kind, count = elem
            agg.setdefault(status, []).append((kind, count))
            agg[status].sort(key=lambda kind_count: kind_count[0].kind)
            return agg

        context.update(reduce(_reduce, pets, {}))

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
