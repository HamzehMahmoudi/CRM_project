from django.db import models
from organization.models import Organization, Product
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()


class QuoteItem(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "product"), on_delete=models.PROTECT)
    qty = models.IntegerField(_("qty"))
    quote = models.ForeignKey(
        "quote.Quote", verbose_name=_("quote"), on_delete=models.CASCADE)
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


class Quote(models.Model):
    organization = models.ForeignKey(Organization, verbose_name=_(
        "organization"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name=_(
        "creator"), on_delete=models.PROTECT)
    created_on = models.DateTimeField(
        _("created on"), auto_now_add=True)

    def __str__(self):
        return f"{self.organization} by {self.user}"

    def merge_items(self):
        for item in self.quoteitem_set.all():
            temp = self.quoteitem_set.filter(
                product=item.product)  # get similar items
            if temp.count() > 1:  # create one Instead of more than one
                p = item.product
                price = temp.aggregate(Sum("price")).get("price__sum", 0)
                qty = temp.aggregate(Sum("qty")).get("qty__sum", 0)
                discount = temp.aggregate(
                    Sum("discount")).get("discount__sum", 0)
                temp.delete()
                QuoteItem(product=p, quote=self,
                          price=price, discount=discount, qty=qty).save()

    @staticmethod
    def clean_list():
        qouts = Quote.objects.all()
        for q in qouts:             # delete quotes that doesnt have any item
            items = q.quoteitem_set.all()
            if items.count() == 0:
                q.delete()

    def get_total_price(self):
        if self.quoteitem_set.aggregate(Sum("price")).get("price__sum", 0) is None:
            return 0
        return self.quoteitem_set.aggregate(Sum("price")).get("price__sum", 0)

    def get_total_discount(self):
        if self.quoteitem_set.aggregate(Sum("discount")).get("discount__sum", 0) is None:
            return 0
        return self.quoteitem_set.aggregate(Sum("discount")).get("discount__sum", 0)
