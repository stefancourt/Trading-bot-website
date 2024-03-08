from django.shortcuts import render, redirect
from trade.models import AAPLStock, MSFTStock
from trade.forms import DateForm, TypeForm, PlaceTradeForm
from main.models import UserProfile, Trades
from django.http import JsonResponse

def trade_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_id = user_profile.user_id
        apple = AAPLStock.objects.all().order_by('-date')
        microsoft = MSFTStock.objects.all().order_by('-date')
        if request.method == "POST":
            form = PlaceTradeForm(request.POST)
            if form.is_valid():
                # Process the form data
                stop_loss = form.cleaned_data['stop_loss']
                take_profit = form.cleaned_data['take_profit']
                order_type = form.cleaned_data['order_type']
            context={
                'place_trade_form': PlaceTradeForm(),
                'date_form': DateForm(),
                'stock_type_form': TypeForm(),
            }
            return JsonResponse({"take_profit":take_profit, "stop_loss":stop_loss, "order_type":order_type, "user_id": user_id})

        else:
            context={
                'place_trade_form': PlaceTradeForm(),
                'date_form': DateForm(),
                'stock_type_form': TypeForm(),
                'apple': "{:.2f}".format(apple[0].close),
                'apple_change': "{:.2f}".format(apple[0].close - apple[1].close),
                'microsoft': "{:.2f}".format(microsoft[0].close),
                'microsoft_change': "{:.2f}".format(microsoft[0].close - microsoft[1].close),
            }
            return render(request, "trade/trade.html", context=context)
    else:
        return redirect('/')
            
