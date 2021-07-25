from organization.models import Organization, Product
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from . import enums

User = get_user_model()


class FollowUp(models.Model):
    """
    model that represent the sale follow up
    """
    report = models.TextField(verbose_name=_("sale report"))
    organization = models.ForeignKey(
        Organization, verbose_name=_("organization"), on_delete=models.PROTECT)
    creator = models.CharField(verbose_name=_("written by"), max_length=50)
    written_on = models.DateTimeField(
        verbose_name=_("written at"), auto_now_add=True)


class Quote(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_(
        "organization"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=_(
        "creator"), on_delete=models.PROTECT)
    created_on = models.DateTimeField(
        _("created on"), auto_now_add=True)

    def __str__(self):
        return f"{self.organization} by {self.user}"


class QuoteItem(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.PROTECT)
    qty = models.IntegerField(_("qty"))
    quote = models.ForeignKey(
        Quote, verbose_name=_("quote"), on_delete=models.CASCADE)
    discount = models.IntegerField(verbose_name=_("discount"), default=0)

    def __str__(self):
        return f"{self.qty} of {self.product}"

    def get_total(self):
        tax = 0
        if self.product.taxable:
            tax = (self.qty * self.product.price) * (9 / 100)

        return (self.qty * self.product.price) + tax - self.discount


class EmailHistory(models.Model):
    reciver = models.ForeignKey(Organization, verbose_name=_(
        "to"), on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=enums.EmailStatus.choices,
        default=enums.EmailStatus.SENT,
    )
    sender = models.ForeignKey(User, verbose_name=_(
        "from"), on_delete=models.PROTECT)
    send_on = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Send at"))

    def __str__(self):
        return f"{self.sender.username} to {self.reciver.name}"
