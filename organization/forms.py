from django.forms import ModelForm
from .models import Organization


class OrganForm(ModelForm):

    class Meta:
        model = Organization
        exclude = ['registered_on', 'creator']
