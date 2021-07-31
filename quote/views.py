from django.core.exceptions import PermissionDenied
from django.db.models.fields import mixins
from django.http.response import Http404
from django.shortcuts import render, redirect
from .models import Quote, QuoteItem
from django.views import generic
from django.contrib.auth import mixins, decorators
import weasyprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from organization import models
from django.forms import formset_factory
from .forms import QuoteitemForm
from django.contrib import messages
# Create your views here.


class QuoteList(mixins.LoginRequiredMixin, generic.ListView):
    """
    show all quotes in list
    """
    model = Quote
    template_name = 'quote/quotlst.html'
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
    organ = models.Organization.objects.get(pk=pk)
    quote = Quote.objects.create(organization=organ, user=request.user)
    quote.save()
    print(f"quote created with id {quote.pk}")
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
        for form in formset:
            if form.is_valid():
                if not form.fields["qty"] or form.fields["product"]:
                    continue
                form.save(commit=False).quote = quote
                form.save()
        messages.info(
            request, "yourselected item added ")
        return redirect('add-item', qid=quote.pk)
    else:
        formset = QuoteitemFormset()
        # user only can chose related products
        formset.empty_form.base_fields["product"].queryset = quote.organization.get_related_product(
        )
        return render(request, 'quote/add_quote.html', {"formset": formset})
