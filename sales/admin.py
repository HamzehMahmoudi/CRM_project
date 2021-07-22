from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.EmailHistory)
admin.site.register(models.FollowUp)
admin.site.register(models.Quote)
admin.site.register(models.QuoteItem)
