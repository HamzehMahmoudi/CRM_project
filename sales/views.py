from django import views
from django.core.exceptions import PermissionDenied
from django.db.models.fields import mixins
from django.http.response import JsonResponse
import organization
from sales.tasks import send_email_task
from django.shortcuts import render, redirect
from .models import Quote, QuoteItem, FollowUp
from django.views import generic
from django.contrib.auth import mixins, decorators
import weasyprint
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_email_task
from organization import models
from django.forms import formset_factory
from .forms import QuoteitemForm
from django.contrib import messages

from sales import forms
# Create your views here.


@decorators.login_required
@csrf_exempt
def email(request):  # send email to company
    qid = request.GET.get('qid')
    send_email_task.delay(request.user.pk, qid)
    return redirect('quotelist')


class QuoteList(mixins.LoginRequiredMixin, generic.ListView):
    """
    show all quotes in list
    """
    model = Quote
    template_name = 'sales/quotlst.html'
    paginate_by = 10

    def get_queryset(self):  # delete empty Quotes
        qs = Quote.objects.filter(user=self.request.user)
        for q in qs:
            q.clean_list()
        return qs


class QuoteDetail(mixins.LoginRequiredMixin, generic.DetailView):
    """
    show quote detail and download quote as PDF
    """
    model = Quote
    template_name = 'sales/quotedetail.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            raise PermissionDenied
        else:
            if self.request.GET.get('act') == 'download':
                # download the file
                g = super().get(request, *args, **kwargs)
                rendered_content = g.rendered_content
                pdf = weasyprint.HTML(string=rendered_content,
                                        base_url="http://127.0.0.1:8000").write_pdf()
                response = HttpResponse(pdf, content_type="application/pdf")
                return response
            else:
                # return html response when user click on eye icon
                return super().get(request, *args, **kwargs)


@decorators.login_required
def create_quote(request, pk):
    organ = models.Organization.objects.get(pk=pk)
    quote = Quote(organization=organ, user=request.user)
    quote.save()
    return redirect('add-item', qid=quote.pk)


def delete_quote_item(request, pk):
    instance = QuoteItem.objects.get(pk=pk)
    qpk = instance.quote.pk
    instance.delete()
    return redirect("quote-detail", pk=qpk)


@decorators.login_required
@csrf_exempt
def add_item(request, qid):
    """
    add item to Quote
    """
    quote = Quote.objects.get(pk=qid)
    QuoteitemFormset = formset_factory(QuoteitemForm, extra=3)
    if request.method == 'POST':
        formset = QuoteitemFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save(commit=False).quote = quote
                form.save()
        if not quote.quoteitem_set.all():
            quote.delete()
        messages.info(
            request, "item added")
        return redirect('add-item', qid=quote.pk)
    else:
        formset = QuoteitemFormset()
        formset.empty_form.base_fields["product"].queryset = quote.organization.get_org_product(            # user only can chose related products
        ).product_set.all()
        return render(request, 'sales/add_quote.html', {"formset": formset})


@decorators.login_required
def add_follow_up(request, orgid):
    organ = models.Organization.objects.get(pk=orgid)
    if request.method == 'POST':
        form = forms.FollowUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.organization = organ
            instance.creator = request.user
            instance.save()
            return redirect('orgdetail', pk=orgid)
    else:
        form = forms.FollowUpForm()
        return render(request, 'sales/add_followup.html', {"form": form})


@decorators.login_required
def show_followup(request):
    orgid = request.GET.get("orgid")
    organ = models.Organization.objects.get(pk=orgid)
    followups = FollowUp.objects.filter(
        organization=organ, creator=request.user)
    return JsonResponse({"result": list(followups.values())})
