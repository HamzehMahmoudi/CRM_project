from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
# Create your models here.

User = get_user_model()


class OrganizationProduct(models.Model):
    """ product that company produce"""
    name = models.CharField(verbose_name=_("Product name"), max_length=50)


class Product(models.Model):
    """our product that we sell to the client"""
    name = models.CharField(verbose_name=_("Product name "), max_length=50)
    price = models.IntegerField(verbose_name=_("Product price"))
    taxable = models.BooleanField(verbose_name=_("Taxable"))
    pdf_catalogue = models.FileField(_("Catalogue (only pdf)"), upload_to=None, max_length=100, validators=[
                                     FileExtensionValidator(allowed_extensions=['pdf'])])  # this method is not safe because its just look at ext of file not magic numbers in binary
    img_catalogue = models.ImageField(verbose_name=_(
        "catalogue (only img)"), upload_to=None, max_length=None)
    technical_info = models.TextField(verbose_name=_("technical information"))
    related_product = models.ManyToManyField(
        OrganizationProduct, verbose_name=_("related product"))


class OrganizationProduct(models.Model):
    """ product that company produce"""
    name = models.CharField(verbose_name=_("Product name"), max_length=50)


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
