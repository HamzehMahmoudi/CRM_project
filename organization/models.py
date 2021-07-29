from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
# Create your models here.

User = get_user_model()

validator = RegexValidator(
    regex="^09\d{9}$", message="invalid phone number")


class OrganizationProduct(models.Model):
    """ product that company produce"""
    name = models.CharField(verbose_name=_("Product name"), max_length=50)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """our product that we sell to the client"""
    name = models.CharField(verbose_name=_("Product name "), max_length=50)
    price = models.IntegerField(verbose_name=_("Product price"))
    taxable = models.BooleanField(verbose_name=_("Taxable"))
    pdf_catalogue = models.FileField(_("Catalogue (only pdf)"), upload_to='pdf/', max_length=100, validators=[
                                     FileExtensionValidator(allowed_extensions=['pdf'])])  # this method is not safe because its just look at ext of file not magic numbers in binary
    img_catalogue = models.ImageField(verbose_name=_(
        "catalogue (only img)"), upload_to="img/", max_length=300)
    technical_info = models.TextField(verbose_name=_("technical information"))
    related_product = models.ManyToManyField(
        OrganizationProduct, verbose_name=_("related product"), blank=True)

    def __str__(self):
        return f"{self.name}"


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
                                   blank=False, verbose_name=_("Agent Phone number"), validators=[validator, ])
    registered_on = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Registered at"))
    products = models.ManyToManyField(
        OrganizationProduct, verbose_name=_("products"))
    creator = models.ForeignKey(
        User, verbose_name=_("added by"), on_delete=models.PROTECT)
    workers = models.IntegerField(verbose_name=_(
        "workers qty"), blank=True, null=True)

    def get_related_product(self):
        products = self.products.all()
        return Product.objects.filter(related_product__in=products).distinct()

    def __str__(self):
        return f'{self.name}-{self.province}'
