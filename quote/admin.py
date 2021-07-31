from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.QuoteItem)
class QuoteItemInline(admin.TabularInline):
    """
    Admin inline for OrderItem model
    """

    model = models.QuoteItem
    fields = [
        "product",
        "qty",
    ]


@admin.register(models.Quote)
class OrderAdmin(admin.ModelAdmin):
    inlines = [QuoteItemInline]
    list_display = [
        "pk",
        "organization",
        "user",
    ]

    list_display_links = [
        "pk",
        "organization",
    ]
    list_filter = ["organization",  "created_on"]
