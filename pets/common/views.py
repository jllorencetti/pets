from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'staticpages/about.html'


def not_found(request):
    return render(request, 'staticpages/404.html')


def home(request):
    return render(request, 'common/home.html')
