from django.shortcuts import render, redirect
from .models import UserProfile, Trades

def stats_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        money_in_account = user_profile.money_in_account

        context = {
            "money_in_account": money_in_account
        }
        return render(request, "main/stats.html", context=context)
    else:
        return redirect("/")