from sales.forms import FollowUpForm
from django.db.models.fields import related
from . import models
from django.shortcuts import redirect, render
from django.views import generic
from .forms import OrganizationForm
from django.core.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from .serializers import OrganSerializar
from rest_framework.exceptions import NotAuthenticated
from django.contrib.auth import mixins


class CreateOrganization(mixins.LoginRequiredMixin, generic.CreateView):
    """
    salesman can add an organization using this view 
    """
    form_class = OrganizationForm
    template_name = "organization/creatorgan.html"
    success_url = 'organlist'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.save()
        return redirect('organlist')


class OrganizationList(mixins.LoginRequiredMixin, generic.ListView):
    """
    view to see all organizations together 
    """
    model = models.Organization
    template_name = "organization/organlist.html"
    paginate_by = 10  # show 10 organization per page

    def get_queryset(self):  # only org creator can see oganization
        return models.Organization.objects.filter(creator=self.request.user)


class OrganizationDetail(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Organization
    extra_context = {"form": FollowUpForm()}

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user == obj.creator:  # only org creator can see details
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied


class OrganizationUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Organization
    form_class = OrganizationForm
    template_name = "organization/organ_edit.html"

    def form_valid(self, form):
        form.save()
        return redirect("orgdetail", pk=self.get_object().pk)


class ProductList(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Product
    paginate_by = 10


class OrganizationListApi(ListAPIView):
    serializer_class = OrganSerializar

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated("You need to Login")
        else:
            return models.Organization.objects.filter(creator=self.request.user)
