from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.FollowUp)


@admin.register(models.EmailHistory)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['sender', 'reciver', 'status']
    list_filter = ['status', 'reciver']
