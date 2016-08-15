from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, \
    UpdateView, View

from braces.views import LoginRequiredMixin

from meupet.forms import SearchForm
from . import forms
from . import models


class PetIndexView(ListView):
    template_name = 'meupet/index.html'
    context_object_name = 'pets'

    def get_queryset(self):
        return models.Pet.objects.select_related('city').order_by('-id')[:12]


def pet_detail_view(request, pk_or_slug):
    pet = models.Pet.objects.filter(slug=pk_or_slug).first()
    if not pet:
        pet = get_object_or_404(models.Pet, pk=pk_or_slug)

    context = {
        'pet': pet,
        'current_url': request.build_absolute_uri(request.get_full_path()),
    }
    return render(request, 'meupet/pet_detail.html', context)


def paginate_pets(queryset, page, paginate_by=12):
    """Returns the pets for the current requested page and the page number"""
    paginator = Paginator(queryset, paginate_by)

    try:
        pets = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
        page = 1
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return pets, page


def render_pet_list(request, kind, status, queryset):
    pets, page = paginate_pets(queryset, request.GET.get('page'))

    return render(request, 'meupet/pet_list.html', {
        'pets': pets,
        'kind': kind,
        'status': status,
        'current_page': page
    })


def lost_pets(request, kind):
    return render_pet_list(
        request,
        kind,
        'Desaparecidos',
        models.Pet.objects.get_lost_or_found(kind)
    )


def adoption_pets(request, kind):
    return render_pet_list(
        request,
        kind,
        'Para Adoção',
        models.Pet.objects.get_for_adoption_adopted(kind)
    )


class RegisterPetView(LoginRequiredMixin, CreateView):
    template_name = 'meupet/register_pet.html'
    model = models.Pet
    form_class = forms.PetForm

    def get_success_url(self):
        return reverse('meupet:registered', args=[self.object.slug])

    def get(self, request, *args, **kwargs):
        if not request.user.is_information_confirmed:
            messages.warning(request, 'Favor confirmar suas informações antes de cadastrar algum pet.')
            return HttpResponseRedirect(reverse('users:edit'))
        else:
            return super(RegisterPetView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RegisterPetView, self).form_valid(form)


class EditPetView(UpdateView):
    template_name = 'meupet/edit.html'
    form_class = forms.PetForm
    model = models.Pet

    def get(self, request, *args, **kwargs):
        current_pet = self.get_object()
        if request.user == current_pet.owner:
            return super(EditPetView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(
                reverse('meupet:detail', kwargs={'pk_or_slug': current_pet.slug})
            )

    def form_valid(self, form):
        return super(EditPetView, self).form_valid(form)


def delete_pet(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)
    if request.method == 'POST' and request.user == pet.owner:
        pet.delete()
        return HttpResponseRedirect(reverse('meupet:index'))
    else:
        return HttpResponseRedirect(pet.get_absolute_url())


def change_status(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)
    pet.change_status()
    return HttpResponseRedirect(reverse('meupet:detail', kwargs={'pk_or_slug': pet.slug}))


def upload_image(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)
    picture = request.FILES.get('another_picture', False)

    if request.user == pet.owner and request.method == 'POST' and picture:
        models.Photo.objects.create(pet_id=pet.id, image=picture)

    return HttpResponseRedirect(reverse('meupet:detail', kwargs={'pk_or_slug': pet.slug}))


class SearchView(View):
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


def registered(request, slug):
    context = {
        'pet_slug': slug,
        'facebook_url': settings.FACEBOOK_SHARE_URL.format(slug),
        'twitter_url': settings.TWITTER_SHARE_URL.format(slug),
    }
    return render(request, 'meupet/registered.html', context)


def poster(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)
    return render(request, 'meupet/poster.html', {'pet': pet})
