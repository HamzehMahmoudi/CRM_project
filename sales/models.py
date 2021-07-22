from organization.models import Organization, Product
from organization.forms import OrganForm
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from . import enums

User = get_user_model()


class FollowUp(models.Model):
    """
    model that represent the sale follow up
    """
    report = models.TextField(verbose_name=_("sale report"))
    creator = models.CharField(verbose_name=_("written by"), max_length=50)
    written_on = models.DateTimeField(
        verbose_name=_("written at"), default=timezone.now())


class Quote(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_(
        "organization"), on_delete=models.PROTECT)


class QuoteItem(models.Model):
    prodduct = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.PROTECT)
    qty = models.IntegerField(_("qty"))
    quote = models.ForeignKey(
        Quote, verbose_name=_("quote"), on_delete=models.CASCADE)


class EmailHistory(models.Model):
    reciver = models.EmailField(verboes_name=_(
        "Reciver"), max_length=254, null=False, blank=False)
    status = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=enums.EmailStatus.choices,
        default=enums.EmailStatus.SENT,
    )
    sender = models.ForeignKey(User, verbose_name=_(
        "Sender"), on_delete=models.PROTECT)
    send_on = models.DateTimeField(
        default=timezone.now(), verbose_name=_("Send at"))
