from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models

@receiver(post_save, sender=models.Organization)
def create_orgproduct(sender, instance, created, **kwargs):
    if created:
        models.OrganizationProduct(name=instance.product).save()
        print("done")
