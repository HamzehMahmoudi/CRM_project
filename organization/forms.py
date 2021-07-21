from django.forms import ModelForm
from .models import Organization


class OrganForm(ModelForm):
    model = Organization

    class Meta:
        exclude = ['registered_on', 'creator']
        