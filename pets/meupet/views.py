from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView, ListView, CreateView, \
    UpdateView, View

from braces.views import LoginRequiredMixin

from common.views import MeuPetEspecieMixin
from . import forms
from . import models
from meupet.forms import SearchForm


class HomePageView(MeuPetEspecieMixin, ListView):
    template_name = 'meupet/index.html'
    context_object_name = 'pets'

    def get_queryset(self):
        return models.Pet.objects.select_related('city').order_by('-id')[:12]


class AboutPageView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/about.html'


class AssociacoesView(MeuPetEspecieMixin, TemplateView):
    template_name = 'staticpages/associacoes.html'


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


class RegisterLostPetView(LoginRequiredMixin, MeuPetEspecieMixin, CreateView):
    template_name = 'meupet/register_pet.html'
    model = models.Pet
    form_class = forms.PetForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_information_confirmed:
            messages.warning(request, 'Favor confirmar suas informações antes de cadastrar algum pet.')
            return HttpResponseRedirect(reverse('users:edit'))
        else:
            return super(RegisterLostPetView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RegisterLostPetView, self).form_valid(form)


class RegisterAdoptionPetView(LoginRequiredMixin, MeuPetEspecieMixin, CreateView):
    template_name = 'meupet/register_pet.html'
    model = models.Pet
    form_class = forms.PetForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_information_confirmed:
            messages.warning(request, 'Favor confirmar suas informações antes de cadastrar algum pet.')
            return HttpResponseRedirect(reverse('users:edit'))
        else:
            return super(RegisterAdoptionPetView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = models.Pet.FOR_ADOPTION
        return super(RegisterAdoptionPetView, self).form_valid(form)


class QuickSearchView(MeuPetEspecieMixin, ListView):
    template_name = 'meupet/index.html'
    context_object_name = 'pets'

    def get(self, request, *args, **kwargs):
        if not request.GET.get('q'):
            return HttpResponseRedirect(reverse('meupet:index'))
        else:
            return super(QuickSearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("q")

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
        form = SearchForm()
        return render(request, 'meupet/search.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            pet_city = form.cleaned_data['city']
            pet_size = form.cleaned_data['size']
            pet_status = form.cleaned_data['status']
            pet_kind = form.cleaned_data['kind']
            pet_sex = form.cleaned_data['sex']

            if not any([pet_size, pet_city, pet_kind, pet_status, pet_sex]):
                messages.error(self.request, 'É necessário selecionar ao menos um filtro')
                return HttpResponseRedirect(reverse('meupet:search'))

            query = Q()

            if pet_city:
                query = query & Q(city=pet_city)
            if pet_size:
                query = query & Q(size=pet_size)
            if pet_status:
                query = query & Q(status=pet_status)
            if pet_kind:
                query = query & Q(kind=pet_kind)
            if pet_sex:
                query = query & Q(sex=pet_sex)

            pets = models.Pet.objects.filter(query)
        else:
            return HttpResponseRedirect(reverse('meupet:search'))

        return render(request, 'meupet/search.html', {'request': request, 'form': form, 'pets': pets})
