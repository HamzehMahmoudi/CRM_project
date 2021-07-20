from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Product(models.Model):
    """our product that we sell to the client"""
    name = models.CharField(verbose_name=_("Product name "), max_length=50)
    qty_in_stock = models.IntegerField(verbose_name=_("Avalable qty"))


class OrganizationProduct(models.Model):
    """ product that company produce"""
    name = models.CharField(verbose_name=_("Product name"), max_length=50)
    related_product = models.ManyToManyField(Product, verbose_name=_(""))


class Organization(models.Model):
    """organization model"""
    name = models.CharField(max_length=50, null=False,
                            blank=False, verbose_name=_("Organization name"))
    province = models.CharField(
        max_length=20, null=False, blank=False, verbose_name=_("Location"))
    phone = models.CharField(max_length=11, null=False,
                             blank=False, verbose_name=_("Phone number"))
    email = models.EmailField(max_length=254, verbose_name=_("Email address"))
    agent = models.CharField(max_length=50, null=False,
                             blank=False, verbose_name=_("Organization agent"))
    agent_phone = models.CharField(max_length=11, null=False,
                                   blank=False, verbose_name=_("Phone number"))
    registered_on = models.DateTimeField(
        default=timezone.now(), verbose_name=_("Registered at"))
    product = models.ForeignKey(
        OrganizationProduct, verbose_name=_("Organization product"))
    creator = models.ForeignKey(
        User, verbose_name=_("added by"), on_delete=models.PROTECT)
