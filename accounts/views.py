from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .models import User
from .forms import RegistrationForm, UserForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm
    template_name = 'registration/new_login.html'


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')


class UserUpdateView(UpdateView, LoginRequiredMixin):
    from_class = UserForm
    template_name = 'accounts/user_update.html'
    sucess_url = 'profile'

