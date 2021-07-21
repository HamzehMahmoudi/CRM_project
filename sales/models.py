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
    pass


class QuoteItem(models.Model):
    pass


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

    pass
