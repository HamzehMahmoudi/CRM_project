from django.core.exceptions import PermissionDenied
from django.db.models.fields import mixins
from django.forms.models import inlineformset_factory
from django.http.response import Http404
from django.shortcuts import render, redirect
from .models import Quote, QuoteItem
from django.views import generic
from django.contrib.auth import mixins, decorators
import weasyprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from organization import models as orgmodel
from django.contrib import messages
from django.forms import inlineformset_factory
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.utils.decorators import method_decorator
from .forms import QuoteItemForm

# Create your views here.


class QuoteList(mixins.LoginRequiredMixin, generic.ListView):
    """
    show all quotes in list
    """
    model = Quote
    template_name = 'quote/quotlst.html'
    paginate_by = 10
    ordering = ["created_on"]

    def get_queryset(self):  # delete empty Quotes
        Quote.clean_list()
        qs = Quote.objects.filter(user=self.request.user)
        return qs


@method_decorator(xframe_options_sameorigin, name='dispatch')
class QuoteDetail(mixins.LoginRequiredMixin, generic.DetailView):
    """

    show quote detail and download quote as PDF
    """
    model = Quote
    template_name = 'quote/quotedetail.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            raise PermissionDenied
        elif not self.get_object():
            raise Http404("ops! the following quote does not exist")
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
    try:
        organ = orgmodel.Organization.objects.get(pk=pk)
        quote = Quote.objects.create(organization=organ, user=request.user)
        quote.save()
        q = Quote.objects.get(pk=quote.pk)
        print(f"quote created with id {quote.pk}")
        return redirect('add-item', qid=q.pk)
    except orgmodel.Organization.DoesNotExist:
        raise Http404("Organization not found")


def delete_quote_item(request, pk):
    instance = QuoteItem.objects.get(pk=pk)
    qpk = instance.quote.pk
    instance.delete()
    return redirect("quote-detail", pk=qpk)


@decorators.login_required
def add_item(request, qid):
    """
    add item to Quote
    """
    try:
        quote = Quote.objects.get(pk=qid)
        QouteFormSet = inlineformset_factory(
            Quote, QuoteItem, fields=('product', 'qty', 'discount'), can_delete=False)
        formset = QouteFormSet(
            queryset=QuoteItem.objects.none(), instance=quote)
        formset.empty_form.base_fields["product"].queryset = quote.organization.get_related_product(
        )
        if request.method == 'POST':
            formset = QouteFormSet(request.POST, instance=quote)
            if formset.is_valid():
                formset.save()
                messages.info(request, "your selected item added ")
                quote.merge_items()
                return redirect('add-item', qid=quote.pk)
        else:
            return render(request, 'quote/add_quote.html', {"formset": formset, "qid": qid})
    except Quote.DoesNotExist:
        raise Http404("Quote not found")


class SelectOrgan(mixins.LoginRequiredMixin, generic.ListView):
    model = orgmodel.Organization
    paginate_by = 10
    ordering = ["registered_on"]
    template_name = "quote/select_organization.html"

    def get_queryset(self):
        return orgmodel.Organization.objects.filter(creator=self.request.user)


class QuoteItemUpdate(mixins.LoginRequiredMixin, generic.UpdateView):
    model = QuoteItem
    form_class = QuoteItemForm
    template_name = "quote/edit_item.html"

    def form_valid(self, form):
        form.save()
        return redirect("quote-detail", self.get_object().quote.pk)

    def get(self, *args, **kwargs):
        if self.request.user != self.get_object().quote.user:
            raise PermissionDenied
        else:
            return super().get(*args, **kwargs)
