from django import forms
from django.db.models import Q
from django.utils.translation import ugettext as _

from meupet import models
from cities.models import City, State
from meupet.models import PetStatus


def _build_choice_field(label, choices=None, required=False):
    empty_choice = (('', '------------'),)
    field = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=label,
        choices=empty_choice,
        required=required
    )
    if choices:
        field.choices += choices
    return field


class PetForm(forms.ModelForm):
    city = _build_choice_field(_('City'), required=True)
    state = _build_choice_field(_('State'), required=True)
    status = _build_choice_field(_('Status'), required=True)

    class Meta:
        model = models.Pet
        fields = ('name', 'description', 'city', 'kind',
                  'profile_picture', 'size', 'sex', 'status',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Costelinha')}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _(
                    "It is black and chubby, very shy, "
                    "has went gone next to the school in downtown. "
                    "There's a slight flaw in the tail fur.")
            }),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
        }

    @staticmethod
    def _get_status_choices(current_status=None):
        status_filter = Q(final=False)
        if current_status:
            status_filter |= Q(id=current_status)
        queryset = models.PetStatus.objects.values_list('id', 'description').filter(status_filter)
        return queryset.order_by('final', 'description')

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        if instance:
            initial['state'] = instance.city.state.code
            initial['city'] = instance.city.code
            initial['status'] = instance.status.id
        kwargs['initial'] = initial
        super(PetForm, self).__init__(*args, **kwargs)

        self.fields['state'].choices += tuple(State.objects.values_list('code', 'name'))
        self.fields['status'].choices += tuple(self._get_status_choices(initial.get('status')))

        state = kwargs['initial'].get('state')
        if 'data' in kwargs:
            state = kwargs['data'].get('state')
        if state:
            self.fields['city'].choices += tuple(City.objects.filter(state__code=state).values_list('code', 'name'))

    def clean_profile_picture(self):
        img = self.cleaned_data.get('profile_picture', False)
        if img and img.size > 8 * 1024 * 1024:
            raise forms.ValidationError(_('Image is larger than the maximum size of 8MB'))
        return img

    def clean_name(self):
        return self.cleaned_data['name'].title()

    def clean_city(self):
        return City.objects.get(code=self.cleaned_data['city'])

    def clean_status(self):
        return PetStatus.objects.get(pk=self.cleaned_data['status'])


class SearchForm(forms.Form):
    city = _build_choice_field(_('City'))
    kind = _build_choice_field(_('Kind'))
    size = _build_choice_field(_('Size'), models.Pet.PET_SIZE)
    status = _build_choice_field(_('Status'))
    sex = _build_choice_field(_('Sex'), models.Pet.PET_SEX)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices += tuple(
            City.objects.filter(pet__active=True).order_by('name').values_list('id', 'name').distinct()
        )
        self.fields['kind'].choices += tuple(models.Kind.objects.values_list('id', 'kind'))
        self.fields['status'].choices += tuple(
            models.PetStatus.objects.values_list('id', 'description').filter(final=False).order_by('description')
        )

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        has_cleaned_filter = any([
            cleaned_data['city'],
            cleaned_data['kind'],
            cleaned_data['sex'],
            cleaned_data['size'],
            cleaned_data['status'],
        ])

        if not has_cleaned_filter:
            raise forms.ValidationError(_('You must select at least one filter'))
