from django.shortcuts import render
from .forms import BaseRegisterForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/posts'

