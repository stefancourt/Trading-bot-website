from django.shortcuts import render, redirect
from trade.models import AAPLStock
from trade.forms import DateForm, TypeForm
from main.models import UserProfile

def aitrade_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_total = user_profile.money_in_account
        context = {
            'money_in_account': "{:.2f}".format(user_total),
        }
        return render(request, "aitrade/ai-trade.html", context=context)
    else:
        return redirect('/')