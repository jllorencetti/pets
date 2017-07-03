from django import forms
from django.utils.translation import ugettext as _

from meupet import models
from cities.models import City, State


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
    state = _build_choice_field(_('State'), required=True)
    city = _build_choice_field(_('City'), required=True)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            initial['state'] = instance.city.state.code
            initial['city'] = instance.city.code
        kwargs['initial'] = initial
        super(PetForm, self).__init__(*args, **kwargs)

        self.fields['state'].choices += tuple(State.objects.values_list('code', 'name'))

        state = kwargs['initial'].get('state', None)
        if 'data' in kwargs:
            state = kwargs['data'].get('state', None)
        if state:
            self.fields['city'].choices += tuple(City.objects.filter(state__code=state).values_list('code', 'name'))

    class Meta:
        model = models.Pet
        fields = ('name', 'description', 'city', 'kind',
                  'profile_picture', 'size', 'sex', 'status',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Costelinha')}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': _(
                                                     "It is black and chubby, very shy, "
                                                     "has went gone next to the school in downtown. "
                                                     "There's a slight flaw in the tail fur.")}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_profile_picture(self):
        img = self.cleaned_data.get('profile_picture', False)
        if img and img.size > 8 * 1024 * 1024:
            raise forms.ValidationError(_('Image is larger than the maximum size of 8MB'))
        return img

    def clean_name(self):
        return self.cleaned_data['name'].title()

    def clean_city(self):
        return City.objects.get(code=self.cleaned_data['city'])


class SearchForm(forms.Form):
    city = _build_choice_field(_('City'))
    kind = _build_choice_field(_('Kind'))
    size = _build_choice_field(_('Size'), models.Pet.PET_SIZE)
    status = _build_choice_field(_('Status'), models.Pet.PET_STATUS)
    sex = _build_choice_field(_('Sex'), models.Pet.PET_SEX)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices += tuple(City.objects.values_list('id', 'name'))
        self.fields['kind'].choices += tuple(models.Kind.objects.values_list('id', 'kind'))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        if not any([cleaned_data['size'], cleaned_data['city'], cleaned_data['kind'],
                    cleaned_data['status'], cleaned_data['sex']]):
            raise forms.ValidationError(_('You must select at least one filter'))
