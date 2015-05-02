from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView

from common.views import get_kind_list, MeuPetEspecieMixin
from users.forms import LoginForm, RegisterForm, UpdateUserForm
from users.models import OwnerProfile


class CreateUserView(MeuPetEspecieMixin, CreateView):
    model = OwnerProfile
    form_class = RegisterForm
    template_name = 'users/create.html'

    def form_valid(self, form):
        form.instance.is_information_confirmed = True
        return super(CreateUserView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Conta criada com sucesso. Obrigado!')
        user = authenticate(
            username=self.request.POST.get('username'),
            password=self.request.POST.get('password1')
        )
        login(self.request, user)
        return reverse('meupet:index')


class EditUserProfileView(MeuPetEspecieMixin, UpdateView):
    template_name = 'users/edit_profile.html'
    model = OwnerProfile
    form_class = UpdateUserForm

    def get_success_url(self):
        messages.success(self.request, 'Alterações gravadas com sucesso.')
        return reverse('meupet:index')

    def get_object(self, queryset=None):
        return self.request.user


def user_login(request):
    context = RequestContext(request)
    context['kind_lost'] = get_kind_list()
    context['kind_adoption'] = get_kind_list()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.data.get('username'),
                                password=form.data.get('password'))
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('meupet:index'))
    else:
        form = LoginForm()
    return render_to_response('users/login.html', {'form': form}, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('meupet:index'))


class UserProfileView(MeuPetEspecieMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['object'] = self.request.user
        context['pets'] = self.request.user.pet_set.all()
        return context


class ProfileDetailView(MeuPetEspecieMixin, DetailView):
    template_name = 'users/profile.html'
    model = OwnerProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['pets'] = self.object.pet_set.all()
        return context


def confirm_information(request):
    """ This check that the user has confirmed the information and
    redirect to the correct view"""
    if request.user:
        if request.user.is_information_confirmed:
            return HttpResponseRedirect(reverse('meupet:index'))
        else:
            return HttpResponseRedirect(reverse('users:edit'))