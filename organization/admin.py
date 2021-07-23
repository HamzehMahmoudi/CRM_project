from django.contrib import admin
from . import models
admin.site.register(models.Organization)
admin.site.register(models.OrganizationProduct)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'taxable',
                    'price', 'pdf_catalogue', 'img_catalogue']
    list_editable = ['taxable', 'price']
    list_filter = ['taxable']
    search_fields = ['name__icontains', 'technical_info__icontains']
    list_display_links = ['id', 'name']
