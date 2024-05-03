from django import forms
from trade.models import NewsStockType

class NewsTypeForm(forms.ModelForm):
    class Meta:
        model = NewsStockType
        fields = {'stock_type'}
        widgets = {
            'stock_type': forms.Select(attrs={'class': 'form-type'})
        }