from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView, ListView, CreateView, \
    UpdateView, View

from braces.views import LoginRequiredMixin

from common.views import MeuPetEspecieMixin, get_lost_kinds, get_adoption_kinds
from . import forms
from . import models
from meupet.forms import SearchForm


class PetIndexView(MeuPetEspecieMixin, ListView):
    template_name = 'meupet/index.html'
    context_object_name = 'pets'

    def get_queryset(self):
        return models.Pet.objects.select_related('city').order_by('-id')[:12]


class PetDetailView(MeuPetEspecieMixin, TemplateView):
    template_name = 'meupet/pet_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PetDetailView, self).get_context_data(**kwargs)
        context['pet'] = get_object_or_404(models.Pet, pk=context['id'])
        context['current_url'] = self.request.build_absolute_uri(self.request.get_full_path())
        return context


class AdoptionPetView(MeuPetEspecieMixin, TemplateView):
    template_name = 'meupet/pet_list.html'

    def get_context_data(self, **kwargs):
        context = super(AdoptionPetView, self).get_context_data(**kwargs)
        context['pets'] = models.Pet.objects.get_for_adoption_adopted(context['id'])
        return context


class LostPetView(MeuPetEspecieMixin, TemplateView):
    template_name = 'meupet/pet_list.html'

    def get_context_data(self, **kwargs):
        context = super(LostPetView, self).get_context_data(**kwargs)
        context['pets'] = models.Pet.objects.get_lost_or_found(context['id'])
        return context


class RegisterPetView(LoginRequiredMixin, MeuPetEspecieMixin, CreateView):
    template_name = 'meupet/register_pet.html'
    model = models.Pet
    form_class = forms.PetForm

    def get_success_url(self):
        return reverse('meupet:registered', args=[self.object.id])

    def get(self, request, *args, **kwargs):
        if not request.user.is_information_confirmed:
            messages.warning(request, 'Favor confirmar suas informações antes de cadastrar algum pet.')
            return HttpResponseRedirect(reverse('users:edit'))
        else:
            return super(RegisterPetView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RegisterPetView, self).form_valid(form)


class QuickSearchView(MeuPetEspecieMixin, ListView):
    template_name = 'meupet/quicksearch.html'
    context_object_name = 'pets'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if not query:
            return

        size_reverse = dict((v.upper(), k) for k, v in models.Pet.PET_SIZE)
        size_key = size_reverse.get(query.upper(), '')

        filters = Q(name__icontains=query) | \
                  Q(description__icontains=query) | \
                  Q(city__city__icontains=query)

        if size_key:
            filters = filters | Q(size=size_key)

        pets = models.Pet.objects.filter(filters)
        return pets


class EditPetView(MeuPetEspecieMixin, UpdateView):
    template_name = 'meupet/edit.html'
    form_class = forms.PetForm
    model = models.Pet

    def get(self, request, *args, **kwargs):
        current_pet = self.get_object()
        if request.user == current_pet.owner:
            return super(EditPetView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('meupet:detail', kwargs={'id': current_pet.id}))

    def form_valid(self, form):
        return super(EditPetView, self).form_valid(form)


def delete_pet(request, pet_id):
    pet = get_object_or_404(models.Pet, pk=pet_id)
    if request.method == 'POST' and request.user == pet.owner:
        pet.delete()
        return HttpResponseRedirect(reverse('meupet:index'))
    else:
        return HttpResponseRedirect(pet.get_absolute_url())


def change_status(request, pet_id):
    pet = get_object_or_404(models.Pet, pk=pet_id)
    pet.change_status()
    return HttpResponseRedirect(reverse('meupet:detail', kwargs={'id': pet_id}))


def upload_image(request, pet_id):
    if request.method == 'POST' and request.FILES.get('another_picture', False):
        picture = request.FILES['another_picture']
        photo = models.Photo(pet_id=pet_id, image=picture)
        photo.save()
    return HttpResponseRedirect(reverse('meupet:detail', kwargs={'id': pet_id}))


class SearchView(MeuPetEspecieMixin, View):
    def get(self, request):
        return render(request, 'meupet/search.html', {'form': SearchForm()})

    def post(self, request):
        form = SearchForm(request.POST)

        if not form.is_valid():
            return render(request, 'meupet/search.html', {'form': form})

        query = self._build_query(form.cleaned_data)

        pets = models.Pet.objects.filter(query)
        return render(request, 'meupet/search.html', {'form': form, 'pets': pets})

    def _build_query(self, cleaned_data):
        query = Q()

        for key, value in cleaned_data.items():
            if value:
                query = query & Q(**{key: value})

        return query


def registered(request, pk):
    context = {
        'pet_id': pk,
        'facebook_url': settings.FACEBOOK_SHARE_URL.format(pk),
        'twitter_url': settings.TWITTER_SHARE_URL.format(pk),
        'kind_adoption': get_adoption_kinds(),
        'kind_lost': get_lost_kinds(),
    }
    return render(request, 'meupet/registered.html', context)
