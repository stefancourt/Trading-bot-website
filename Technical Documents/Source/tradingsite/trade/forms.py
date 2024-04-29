from django import forms
from trade.models import StockType

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-date'}))

class AmountForm(forms.Form):
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-amount'}))

class AITypeForm(forms.Form):
    order_type = forms.ChoiceField(
        choices=[('ma', 'Moving Average'), ('rsi', 'RSI'), ('adx', 'ADX'), ('combination', 'Combination')],
        widget=forms.RadioSelect(attrs={'class': 'radio-input'}),
        label=None
    )


class TypeForm(forms.ModelForm):
    class Meta:
        model = StockType
        fields = {'stock_type'}
        widgets = {
            'stock_type': forms.Select(attrs={'class': 'form-type'})
        }

class PlaceTradeForm(forms.Form):
    amount = forms.DecimalField(label='Amount', widget=forms.TextInput(attrs={'class': 'form-control'}))
    take_profit = forms.DecimalField(label='Take Profit', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stop_loss = forms.DecimalField(label='Stop Loss', widget=forms.TextInput(attrs={'class': 'form-control'}))
    order_type = forms.ChoiceField(
        choices=[('buy', 'Buy'), ('sell', 'Sell')],
        widget=forms.RadioSelect(attrs={'class': 'radio-input'}),
        label=''
    )
