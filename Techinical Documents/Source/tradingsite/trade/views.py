from django.shortcuts import render, redirect
from trade.models import AAPLStock
from trade.forms import DateForm, TypeForm, PlaceTradeForm
from main.models import UserProfile, Trades
from datetime import datetime
from django.http import JsonResponse

def trade_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_id = user_profile.user_id
        if request.method == "POST":
            form = PlaceTradeForm(request.POST)
            if form.is_valid():
                # Process the form data
                stop_loss = form.cleaned_data['stop_loss']
                take_profit = form.cleaned_data['take_profit']
                order_type = form.cleaned_data['order_type']
            stock = AAPLStock.objects.all()
            start = request.GET.get('start')
            stock_type = request.GET.get('stock_type')

            if start:
                start = datetime.strptime(start, '%Y-%m-%d')
                stock = stock.filter(date__gte=start)

            context={
                'place_trade_form': PlaceTradeForm(),
                'date_form': DateForm(),
                'stock_type_form': TypeForm(),
            }
            return JsonResponse({"take_profit":take_profit, "stop_loss":stop_loss, "order_type":order_type, "user_id": user_id})

        else:
            stock = AAPLStock.objects.all()
            start = request.GET.get('start')
            stock_type = request.GET.get('stock_type')

            if start:
                start = datetime.strptime(start, '%Y-%m-%d')
                stock = stock.filter(date__gte=start)

            context={
                'place_trade_form': PlaceTradeForm(),
                'date_form': DateForm(),
                'stock_type_form': TypeForm(),
                'result': user_id
            }
            return render(request, "trade/trade.html", context=context)
    else:
        return redirect('/')
            
