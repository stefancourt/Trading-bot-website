from django import forms

CHART_CHOICES =(
    ("Pie","Pie Chart"),
    ("Bar","Bar Chart"),
    ("Polar","Polar Area Chart"),
    ("Radar","Radar Chart"),
)

class ManageForm(forms.Form):
    rent = forms.IntegerField(label="Rent")
    bills = forms.IntegerField(label="Bills")
    food = forms.IntegerField(label="Food")
    invest = forms.IntegerField(label="Invest")
    savings = forms.IntegerField(label="Savings")
    luxury = forms.IntegerField(label="Luxury")
    choices =forms.ChoiceField(choices=CHART_CHOICES)
