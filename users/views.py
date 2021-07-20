from django.shortcuts import render
from .forms import UserRegisterForm
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.


# login and logout views represented using django views
class Register(generic.CreateView):
    """
    registeter a user to login 
    """
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm


class Index(generic.TemplateView):
    """
    this view show the index page 
    """
    template_name = 'users/index.html'
