from django.shortcuts import render
import plotly.express as px
from trade.models import Stock
from trade.forms import DateForm, TypeForm

def trade_view(request):
    stock = Stock.objects.all()
    start = request.GET.get('start')
    end = request.GET.get('end')
    stock_type = request.GET.get('stock_type')

    if start:
        stock = stock.filter(date__gte=start)
    if end:
        stock = stock.filter(date__lte=end)


    fig = px.line(
        x=[c.date for c in stock],
        y=[c.close for c in stock]
    )

    fig.update_layout(
    margin=dict(l=70,r=40,b=0,t=0),
    paper_bgcolor='rgb(185, 227, 241)'
    )

    chart = fig.to_html()

    context={
        'chart': chart,
        'date_form': DateForm(),
        'stock_type_form': TypeForm(),
    }
    return render(request, "trade/trade.html", context)

    
