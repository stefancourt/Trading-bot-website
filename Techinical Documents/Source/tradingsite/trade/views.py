from django.shortcuts import render
from trade.models import AAPLStock
from trade.forms import DateForm, TypeForm
from datetime import datetime

def trade_view(request):
    stock = AAPLStock.objects.all()
    start = request.GET.get('start')
    stock_type = request.GET.get('stock_type')

    if start:
        start = datetime.strptime(start, '%Y-%m-%d')
        stock = stock.filter(date__gte=start)

    context={
        'date_form': DateForm(),
        'stock_type_form': TypeForm(),
    }
    return render(request, "trade/trade.html", context)

    
