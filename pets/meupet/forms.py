from django import forms
from django.utils.translation import ugettext as _

from meupet import models


def _build_choice_field(label, choices=None):
    empty_choice = (('', '------------'),)
    field = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=label,
        choices=empty_choice,
        required=False
    )
    if choices:
        field.choices += choices
    return field


class PetForm(forms.ModelForm):
    new_city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('São Paulo')}
    ))

    class Meta:
        model = models.Pet
        fields = ('name', 'description', 'city', 'kind',
                  'profile_picture', 'size', 'sex', 'status',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Costelinha')}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'placeholder': _(
                                                     "It is black and chubby, very shy, "
                                                     "disappeared next to the school in downtown."
                                                     "There's a slight flaw in the tail fur.")}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(PetForm, self).clean()
        if cleaned_data.get('new_city'):
            new_city, _ = models.City.objects.get_or_create(
                city=cleaned_data.get('new_city').title()
            )
            self.cleaned_data['city'] = new_city
            self.errors.pop('city', None)

    def clean_profile_picture(self):
        img = self.cleaned_data.get('profile_picture', False)
        if img and img.size > 8 * 1024 * 1024:
            raise forms.ValidationError(_('Image is larger than the maximum size of 8MB'))
        return img

    def clean_name(self):
        return self.cleaned_data['name'].title()


class SearchForm(forms.Form):
    city = _build_choice_field(_('City'))
    kind = _build_choice_field(_('Kind'))
    size = _build_choice_field(_('Size'), models.Pet.PET_SIZE)
    status = _build_choice_field(_('Status'), models.Pet.PET_STATUS)
    sex = _build_choice_field(_('Sex'), models.Pet.PET_SEX)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices += tuple(models.City.objects.values_list('id', 'city'))
        self.fields['kind'].choices += tuple(models.Kind.objects.values_list('id', 'kind'))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        if not any([cleaned_data['size'], cleaned_data['city'], cleaned_data['kind'],
                    cleaned_data['status'], cleaned_data['sex']]):
            raise forms.ValidationError(_('You must select at least one filter'))
