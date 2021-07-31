from organization.models import Organization
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


class EmailHistory(models.Model):
    reciver = models.ForeignKey(Organization, verbose_name=_(
        "to"), on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        verbose_name=_("status"),
        choices=enums.EmailStatus.choices,
        default=enums.EmailStatus.FAILED,
    )
    sender = models.ForeignKey(User, verbose_name=_(
        "from"), on_delete=models.PROTECT)
    send_on = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Send at"))

    def __str__(self):
        return f"{self.sender.username} to {self.reciver.name}"
