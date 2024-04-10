from django.shortcuts import render, redirect
from trade.models import AAPLStock, MSFTStock
from trade.forms import DateForm, TypeForm
from main.models import UserProfile

def aitrade_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_total = user_profile.money_in_account
        user_id = user_profile.user_id
        apple = AAPLStock.objects.all().order_by('-date')
        microsoft = MSFTStock.objects.all().order_by('-date')
        context={
            'money_in_account': "{:.2f}".format(user_total),
            'date_form': DateForm(),
            'stock_type_form': TypeForm(),
            'apple': "{:.2f}".format(apple[0].close),
            'apple_change': "{:.2f}".format(apple[0].close - apple[1].close),
            'microsoft': "{:.2f}".format(microsoft[0].close),
            'microsoft_change': "{:.2f}".format(microsoft[0].close - microsoft[1].close),
        }
        return render(request, "aitrade/ai-trade.html", context=context)
    else:
        return redirect('/')