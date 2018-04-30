from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import pgettext, ugettext as _
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    View,
)

from meupet import forms, models
from meupet.forms import SearchForm
from meupet.models import StatusGroup


class PetIndexView(ListView):
    template_name = 'meupet/index.html'
    context_object_name = 'pets'

    def get_queryset(self):
        return models.Pet.objects.select_related('city').order_by('-id')[:12]


def pet_detail_view(request, pk_or_slug):
    pet = models.Pet.objects.filter(slug=pk_or_slug).first()

    if not pet:
        try:
            pet = models.Pet.objects.get(pk=pk_or_slug)
        except ValueError:
            raise Http404()

    context = {
        'pet': pet,
        'pet_url': request.build_absolute_uri(reverse('meupet:detail', args=[pet.slug])),
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


def pet_list(request, group, kind):
    group = StatusGroup.objects.get(slug=group)
    queryset = models.Pet.objects.select_related('city')
    queryset = queryset.filter(active=True)
    queryset = queryset.filter(status__in=group.statuses.all(), kind__slug=kind)

    pets, page = paginate_pets(queryset, request.GET.get('page'))

    return render(request, 'meupet/pet_list.html', {
        'pets': pets,
        'kind': kind,
        'status': group.name,
        'current_page': page
    })


class RegisterPetView(LoginRequiredMixin, CreateView):
    template_name = 'meupet/register_pet.html'
    model = models.Pet
    form_class = forms.PetForm

    def get_success_url(self):
        return reverse('meupet:registered', args=[self.object.slug])

    def get(self, request, *args, **kwargs):
        if not request.user.is_information_confirmed:
            messages.warning(request, _('Please confirm your informations before registering a new pet.'))
            return HttpResponseRedirect(reverse('users:edit'))
        else:
            return super(RegisterPetView, self).get(request, *args, **kwargs)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.info(request, _('You already have a pet registered with this name.'))
            return HttpResponseRedirect(reverse('users:profile'))

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


@require_POST
def delete_pet(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)

    if request.user == pet.owner:
        pet.delete()
        return HttpResponseRedirect(reverse('meupet:index'))

    return HttpResponseRedirect(pet.get_absolute_url())


@require_POST
def change_status(request, slug):
    pet = get_object_or_404(models.Pet, slug=slug)

    if request.user != pet.owner:
        return HttpResponseRedirect(pet.get_absolute_url())

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

        pets = models.Pet.objects.actives().filter(query)
        return render(request, 'meupet/search.html', {'form': form, 'pets': pets})

    @staticmethod
    def _build_query(cleaned_data):
        query = Q()

        for key, value in cleaned_data.items():
            if value:
                query &= Q(**{key: value})

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


def update_register(request, request_key):
    pet = get_object_or_404(models.Pet, request_key=request_key)
    pet.activate()
    return HttpResponseRedirect(pet.get_absolute_url())
