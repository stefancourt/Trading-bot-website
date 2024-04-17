from django import forms
from trade.models import StockType

class OverallTypeForm(forms.ModelForm):
    class Meta:
        model = StockType
        fields = ['stock_type']
        widgets = {
            'stock_type': forms.Select(attrs={'class': 'form-type', 'placeholder': 'Overall'})
        }
    def __init__(self, *args, **kwargs):
        super(OverallTypeForm, self).__init__(*args, **kwargs)
        self.fields['stock_type'].required = False