from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Quote, EmailHistory
from django.template.loader import render_to_string
from django.views import generic
from django.utils.html import strip_tags
import weasyprint
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def email(request):
    qid = request.GET.get('qid')
    quote = Quote.objects.get(id=qid)
    subject = 'this is your Quote'
    context = {"object": quote}
    html = render_to_string('sales/quotedetail.html', context=context)
    text_content = strip_tags(html)
    sender = settings.EMAIL_HOST_USER
    email = quote.organization.email
    msg = EmailMultiAlternatives(subject, text_content, sender, [email])
    msg.attach_alternative(html, "text/html")
    msg.send()
    EmailHistory(sender=request.user, reciver=quote.organization).save()
    return redirect('qoutelist')


class QuoteList(generic.ListView):
    model = Quote
    template_name = 'sales/quotlst.html'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)


class QuoteDetail(generic.DetailView):
    model = Quote
    template_name = 'sales/quotedetail.html'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('act') == 'view':
            # return html response when user click on eye icon
            return super().get(request, *args, **kwargs)
        else:    # download the file
            g = super().get(request, *args, **kwargs)
            rendered_content = g.rendered_content
            pdf = weasyprint.HTML(string=rendered_content,
                                  base_url="http://127.0.0.1:8000").write_pdf()
            response = HttpResponse(pdf, content_type="application/pdf")
            return response
