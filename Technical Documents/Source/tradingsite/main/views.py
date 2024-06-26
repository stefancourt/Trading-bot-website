from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Trades
from .forms import OverallTypeForm
import plotly.graph_objects as go


def stats_view(request):
    if request.user.is_authenticated:
        # Obtains the user logged in
        user_profile = UserProfile.objects.get(user=request.user)
        money_in_account = user_profile.money_in_account
        stock_type = request.GET.get('stock_type')
        if stock_type:
            previous_trades = Trades.objects.filter(user=request.user, stock_name=stock_type)
        else:
            previous_trades = Trades.objects.filter(user=request.user)
        reversed_previous_trades = list(reversed(previous_trades))

        # Plots the waterfall graph on the page
        fig = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = [],
            x = [f"{i+1}" for i in range(len(previous_trades))],
            textposition = "outside",
            text = [],
            y = [trade.pnl for trade in previous_trades],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))

        # Settings for the waterfall graph
        fig.update_layout(
            title="Previous Trades Analysis",
            xaxis_title="Trades",
            yaxis_title="Profit/Loss",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        # Convert the Plotly figure to html for passing to the template
        chart = fig.to_html()


        context = {
            "money_in_account": "{:.2f}".format(money_in_account),
            'stock_type_form': OverallTypeForm(),
            "chart": chart
        }

        # Shows latest trades for the user up to 10 trades
        for i in range(min(len(reversed_previous_trades), 10)):
            context[f"trade_{i+1}"] =f"Trade {i+1}: " + "{:.2f}".format(reversed_previous_trades[i].pnl)
        if len(reversed_previous_trades) != 0:
            # So that it is the total pnl of the user over all stocks
            previous_trades = Trades.objects.filter(user=request.user)
            reversed_previous_trades = list(reversed(previous_trades))
            context["last_trade"] = "{:.2f}".format(reversed_previous_trades[0].total_pnl)
        
        return render(request, "main/stats.html", context=context)
    else:
        # Returns the user to the login/sign-up page if not logged in
        return redirect("/")