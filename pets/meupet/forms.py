from django import forms

from meupet.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'description', 'city', 'kind', 'profile_picture', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
        }
