from quote.models import QuoteItem
from django import forms


class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = QuoteItem
        fields = ("product", "qty", "discount")
