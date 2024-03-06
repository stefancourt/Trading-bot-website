from django import forms
from trade.models import StockType

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class TypeForm(forms.ModelForm):
    class Meta:
        model = StockType
        fields = {'stock_type'}
        widget=forms.Select(attrs={'class': 'form-control'})

class PlaceTradeForm(forms.Form):
    take_profit = forms.DecimalField(label='Take Profit')
    stop_loss = forms.DecimalField(label='Stop Loss')
    order_type = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')], widget=forms.RadioSelect, label='Order Type')
