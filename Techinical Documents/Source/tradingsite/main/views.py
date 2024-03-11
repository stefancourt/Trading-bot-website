from django.shortcuts import render, redirect
from .models import UserProfile, Trades
import plotly.graph_objects as go

def stats_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        money_in_account = user_profile.money_in_account
        previous_trades = Trades.objects.filter(user=request.user)
        reversed_previous_trades = list(reversed(previous_trades))

        fig = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = [],
            x = [f"{i+1}" for i in range(len(previous_trades))],
            textposition = "outside",
            text = [],
            y = [trade.pnl for trade in previous_trades],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

        fig.update_layout(
            title="Previous Trades Analysis",
            xaxis_title="Trades",
            yaxis_title="Profit/Loss",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

        # Convert the Plotly figure to JSON for passing to the template
        chart = fig.to_html()


        context = {
            "money_in_account": "{:.2f}".format(money_in_account),
            "last_trade": "{:.2f}".format(reversed_previous_trades[0].total_pnl),
            "trade_1": "{:.2f}".format(reversed_previous_trades[0].pnl),
            "trade_2": "{:.2f}".format(reversed_previous_trades[1].pnl),
            "trade_3": "{:.2f}".format(reversed_previous_trades[2].pnl),
            "trade_4": "{:.2f}".format(reversed_previous_trades[3].pnl),
            "trade_5": "{:.2f}".format(reversed_previous_trades[4].pnl),
            "trade_6": "{:.2f}".format(reversed_previous_trades[5].pnl),
            "trade_7": "{:.2f}".format(reversed_previous_trades[6].pnl),
            "trade_8": "{:.2f}".format(reversed_previous_trades[7].pnl),
            "trade_9": "{:.2f}".format(reversed_previous_trades[8].pnl),
            "trade_10": "{:.2f}".format(reversed_previous_trades[9].pnl),
            "chart": chart
        }
        return render(request, "main/stats.html", context=context)
    else:
        return redirect("/")