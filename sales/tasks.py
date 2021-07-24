from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Quote, EmailHistory
from .enums import EmailStatus
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model


@shared_task(serializer='json')
def send_email_task(uid, qid):
    try:
        user = get_user_model().objects.get(pk=uid)
        quote = Quote.objects.get(id=qid)
        subject = 'this is your Quote'
        context = {"object": quote}
        html = render_to_string('sales/quotedetail.html', context=context)
        text_content = strip_tags(html)
        sender = settings.EMAIL_HOST_USER
        reciver = quote.organization.email
        msg = EmailMultiAlternatives(subject, text_content, sender, [reciver])
        msg.attach_alternative(html, "text/html")
        msg.send()
        EmailHistory(sender=user, reciver=quote.organization).save()
    except:  # if any exception happend create an EmailHistory object and set Status NOt_SEND
        EmailHistory(sender=user, reciver=quote.organization,
                     status=EmailStatus.NOT_SEND).save()
