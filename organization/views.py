from django.db.models.fields import related
from . import models
from django.shortcuts import redirect, render
from django.views import generic
from .forms import OrganForm


class CreateOragan(generic.CreateView):
    """
    salesman can add an organization using this view 
    """
    form_class = OrganForm
    template_name = "organization/creatorgan.html"
    success_url = 'organlist'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.save()
        return redirect('organlist')


class Organlist(generic.ListView):
    """
    view to see all organizations together 
    """
    model = models.Organization
    template_name = "organization/organlist.html"
    paginate_by = 10  # show 10 organization per page


class OrgDetail(generic.DetailView):
    model = models.Organization
