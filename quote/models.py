from django.db import models
from organization.models import Organization, Product
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.db.models import Sum
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

    @staticmethod
    def clean_list():
        qouts = Quote.objects.all()
        for q in qouts:             # delete quotes that doesnt have any item
            items = q.quoteitem_set.all()
            if items.count() == 0:
                q.delete()

    def get_total_price(self):
        return self.quoteitem_set.aggregate(Sum("price")).get("price__sum", 0)

    def get_total_discount(self):
        return self.quoteitem_set.aggregate(Sum("discount")).get("discount__sum", 0)


class QuoteItem(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.PROTECT)
    qty = models.IntegerField(_("qty"))
    quote = models.ForeignKey(
        Quote, verbose_name=_("quote"), on_delete=models.CASCADE)
    discount = models.IntegerField(verbose_name=_("discount"), default=0)
    price = models.IntegerField(_("price"), default=0)

    def __str__(self):
        return f"{self.qty} of {self.product}"

    def get_price(self):
        tax = 0
        if self.product.taxable:
            tax = (self.qty * self.product.price) * (9 / 100)

        return (self.qty * self.product.price) + tax

    def save(self, *args, **kwargs):
        self.price = self.get_price()
        super(QuoteItem, self).save()
