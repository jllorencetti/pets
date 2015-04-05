from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from users.models import OwnerProfile


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = OwnerProfile
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', 'Efetuar Login'))


class RegisterForm(UserCreationForm):
    class Meta:
        model = OwnerProfile
        fields = ('first_name', 'last_name', 'email', 'username', 'facebook', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            Field('facebook', placeholder=_('Insira o endereço completo do seu perfil no Facebook.')),
            'password1',
            'password2'
        )
        self.helper.add_input(Submit('register', 'Criar Conta'))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ('first_name', 'last_name', 'email', 'facebook', )

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Gravar Alterações'))

    def save(self, commit=True):
        self.instance.is_information_confirmed = True
        super(UpdateUserForm, self).save()