from django import forms
from . import models


class QuoteitemForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['qty'].required = True

    class Meta:
        model = models.QuoteItem
        exclude = ['quote', 'created_on']
        fields = ['product', 'qty', 'discount']
