from django import forms

from meupet import models


class PetForm(forms.ModelForm):
    new_city = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nome da cidade'}
    ))

    class Meta:
        model = models.Pet
        fields = ('name', 'description', 'city', 'kind',
                  'profile_picture', 'size', 'sex', 'status',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
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


class SearchForm(forms.Form):
    empty_choice = (('', '------------'),)

    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='Cidade',
                             required=False)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='Espécie',
                             required=False)
    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='Tamanho',
                             choices=empty_choice + models.Pet.PET_SIZE,
                             required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               label='Status',
                               choices=empty_choice + models.Pet.PET_STATUS,
                               required=False)
    sex = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                            label='Sexo',
                            choices=empty_choice + models.Pet.PET_SEX,
                            required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = self.empty_choice + \
            tuple(models.City.objects.values_list('id', 'city'))
        self.fields['kind'].choices = self.empty_choice + \
            tuple(models.Kind.objects.values_list('id', 'kind'))
