from django.db import models
from organization.models import Organization, Product
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Quote(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_(
        "organization"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=_(
        "creator"), on_delete=models.PROTECT)
    created_on = models.DateTimeField(
        _("created on"), auto_now_add=True)

    def __str__(self):
        return f"{self.organization} by {self.user}"

    def clean_list(self):  # delete quotes that doesnt have any item
        items = self.quoteitem_set.all()
        if items.count() == 0:
            self.delete()


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
