from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Quote, EmailHistory
from django.template.loader import render_to_string
from django.views import generic
# Create your views here.


def email(request, qid):
    quote = Quote.objects.get(id=qid)
    subject = 'Thank you for registering to our site'
    context = {}
    message_html = render_to_string('sales/email.html', context=context)
    sender = settings.EMAIL_HOST_USER
    email = quote.organization.email
    msg = EmailMessage(subject=subject, body=message_html,
                       from_email=sender, bcc=[email, ])
    msg.send()
    EmailHistory(sender=request.user, reciver=email).save()
    return redirect('index')


class QuoteList(generic.ListView):
    model = Quote
    template_name = 'sales/quotlst.html'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)
