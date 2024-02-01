from django.shortcuts import render

def trade_view(request):
    return render(request, "trade/trade.html", context={})