from organization.models import Organization
from django.shortcuts import redirect, render
from django.views import generic
from .forms import OrganForm


class CreateOragan(generic.CreateView):
    """
    salesman can add an organization using this view 
    """
    form_class = OrganForm
    template_name = "organization/creatorgan.html"

    def form_valid(self, form):
        instance = form.save(commit=False).creator
        instance.creator = self.request.user
        instance.save()
        return redirect('organlist')


class Organlist(generic.ListView):
    """
    view to see all organizations together 
    """
    model = Organization
    template_name = "organization/organlist.html"
    paginate_by = 10  # show 10 organization per page
