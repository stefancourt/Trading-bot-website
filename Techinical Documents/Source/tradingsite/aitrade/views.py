from django.shortcuts import render, redirect
from trade.models import AAPLStock, MSFTStock
from trade.forms import DateForm, TypeForm, AmountForm, AITypeForm
from main.models import UserProfile, Trades
from django.http import JsonResponse

def aitrade_view(request):
    if request.user.is_authenticated:
        # Obtains the user logged in
        user_profile = UserProfile.objects.get(user=request.user)
        user_total = user_profile.money_in_account
        user_id = user_profile.user_id
        # Pre-processing to allow previous trades
        previous_trades = Trades.objects.filter(user=request.user)
        reversed_previous_trades = list(reversed(previous_trades))
        # Reverse the list to obtain the latest stock
        apple = AAPLStock.objects.all().order_by('-date')
        microsoft = MSFTStock.objects.all().order_by('-date')
        if request.method == "POST":
            context={
            'date_form': DateForm(),
            'ai_type_form': AITypeForm(),
            'stock_type_form': TypeForm(),
            'amount_form': AmountForm(),
            }
            return JsonResponse({"user_id": user_id})
        else:
            context={
                'money_in_account': "{:.2f}".format(user_total),
                'date_form': DateForm(),
                'ai_type_form': AITypeForm(),
                'stock_type_form': TypeForm(),
                'amount_form': AmountForm(),
                'apple': "{:.2f}".format(apple[0].close),
                'apple_change': "{:.2f}".format(apple[0].close - apple[1].close),
                'microsoft': "{:.2f}".format(microsoft[0].close),
                'microsoft_change': "{:.2f}".format(microsoft[0].close - microsoft[1].close),
            }

            # Shows latest trades for the user up to 9 trades
            for i in range(min(len(reversed_previous_trades), 9)):
                context[f"trade_{i+1}"] =f"Trade {i+1}: " + "{:.2f}".format(reversed_previous_trades[i].pnl)
            if len(reversed_previous_trades) != 0:
                context["last_trade"] = "{:.2f}".format(reversed_previous_trades[0].total_pnl)
                
        return render(request, "aitrade/ai-trade.html", context=context)
    else:
        # Returns the user to the login/sign-up page if not logged in
        return redirect('/')