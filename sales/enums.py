from django.db import models
from django.utils.translation import ugettext as _


class EmailStatus(models.TextChoices):
    """
    Status an Email can have
    """

    SENT = "SENT", _("Sent")
    NOT_SEND = "NOT_SEND", _("NotSend")
