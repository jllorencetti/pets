from django import forms

from meupet.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'description', 'kind', 'profile_picture', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
        }

