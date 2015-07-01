from django import forms

from meupet import models


class PetForm(forms.ModelForm):
    class Meta:
        model = models.Pet
        fields = ('name', 'description', 'city', 'kind', 'profile_picture',
                  'size', 'sex',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    empty_choice = (('', '------------'),)
    city_choices = tuple(models.Pet.objects.values_list('city', 'city').distinct('city'))
    kind_choices = tuple(models.Kind.objects.values_list('id', 'kind'))
    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='Cidade',
                             choices=empty_choice + city_choices,
                             required=False)
    kind = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='Espécie',
                             choices=empty_choice + kind_choices,
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
