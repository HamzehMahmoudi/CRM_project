from django.contrib import admin
from . import models
admin.site.register(models.Organization)
admin.site.register(models.OrganizationProduct)
admin.site.register(models.Product)
