from django import forms

CHART_CHOICES =(
    ("Pie","Pie Chart"),
    ("Bar","Bar Chart"),
    ("Polar","Polar Area Chart"),
    ("Radar","Radar Chart"),
)

class ManageForm(forms.Form):
    rent = forms.IntegerField(label="Rent", widget=forms.TextInput(attrs={'class': 'form-control'}))
    bills = forms.IntegerField(label="Bills", widget=forms.TextInput(attrs={'class': 'form-control'}))
    food = forms.IntegerField(label="Food", widget=forms.TextInput(attrs={'class': 'form-control'}))
    invest = forms.IntegerField(label="Invest", widget=forms.TextInput(attrs={'class': 'form-control'}))
    savings = forms.IntegerField(label="Savings", widget=forms.TextInput(attrs={'class': 'form-control'}))
    luxury = forms.IntegerField(label="Luxury", widget=forms.TextInput(attrs={'class': 'form-control'}))
    choices = forms.ChoiceField(choices=CHART_CHOICES, widget=forms.Select(attrs={'class': 'form-select third'}))
