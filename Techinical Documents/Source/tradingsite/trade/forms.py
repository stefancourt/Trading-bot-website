from django import forms
from trade.models import StockType

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-date'}))

class TypeForm(forms.ModelForm):
    class Meta:
        model = StockType
        fields = {'stock_type'}
        widgets = {
            'stock_type': forms.Select(attrs={'class': 'form-type'})
        }

class PlaceTradeForm(forms.Form):
    take_profit = forms.DecimalField(label='Take Profit', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stop_loss = forms.DecimalField(label='Stop Loss', widget=forms.TextInput(attrs={'class': 'form-control'}))
    order_type = forms.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell')],
        widget=forms.RadioSelect(attrs={'class': 'radio-input'}),
        label='Order Type'
    )
