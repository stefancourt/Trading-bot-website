from django.shortcuts import render, redirect
from trade.models import AAPLStock, MSFTStock
from trade.forms import DateForm, TypeForm, PlaceTradeForm
from main.models import UserProfile
from django.http import JsonResponse

def trade_view(request):
    if request.user.is_authenticated:
        # Obtains the user logged in
        user_profile = UserProfile.objects.get(user=request.user)
        user_total = user_profile.money_in_account
        user_id = user_profile.user_id
        # pre-processing to obtain the latest stock price in the dataset
        apple = AAPLStock.objects.all().order_by('-date')
        microsoft = MSFTStock.objects.all().order_by('-date')
        if request.method == "POST":
            form = PlaceTradeForm(request.POST)
            if form.is_valid():
                # Process the form data
                amount = form.cleaned_data['amount']
                stop_loss = form.cleaned_data['stop_loss']
                take_profit = form.cleaned_data['take_profit']
                order_type = form.cleaned_data['order_type']
            # Other data is not sent as it is always sent when the page is first opened
            context={
                'place_trade_form': PlaceTradeForm(),
                'date_form': DateForm(),
                'stock_type_form': TypeForm(),
            }
            # If a post request is submitted data is sent to the js console
            return JsonResponse({"amount": amount,"take_profit":take_profit, "stop_loss":stop_loss, "order_type":order_type, "user_id": user_id})

        else:
            context={
                'money_in_account': "{:.2f}".format(user_total),
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
        # Returns the user to the login/sign-up page if not logged in
        return redirect('/')
            
