from django.shortcuts import render, redirect
from trade.models import AAPLStock, MSFTStock, JNJStock, PFEStock, JPMStock, BACStock,  AMZNStock, NVDAStock, TSLAStock, METAStock, XOMStock,  PEPStock
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
        jnj = JNJStock.objects.all().order_by('-date')
        pfe = PFEStock.objects.all().order_by('-date')
        jpm = JPMStock.objects.all().order_by('-date')
        bac = BACStock.objects.all().order_by('-date')
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
                'jnj': "{:.2f}".format(jnj[0].close),
                'jnj_change': "{:.2f}".format(jnj[0].close - jnj[1].close),
                'pfe': "{:.2f}".format(pfe[0].close),
                'pfe_change': "{:.2f}".format(pfe[0].close - pfe[1].close),
                'jpm': "{:.2f}".format(jpm[0].close),
                'jpm_change': "{:.2f}".format(jpm[0].close - jpm[1].close),
                'bac': "{:.2f}".format(bac[0].close),
                'bac_change': "{:.2f}".format(bac[0].close - bac[1].close),
                'amazon': "{:.2f}".format(AMZNStock.objects.first().close),
                'amazon_change': "{:.2f}".format(AMZNStock.objects.last().close - AMZNStock.objects.first().close),
                'nvidia': "{:.2f}".format(NVDAStock.objects.first().close),
                'nvidia_change': "{:.2f}".format(NVDAStock.objects.last().close - NVDAStock.objects.first().close),
                'tesla': "{:.2f}".format(TSLAStock.objects.first().close),
                'tesla_change': "{:.2f}".format(TSLAStock.objects.last().close - TSLAStock.objects.first().close),
                'meta': "{:.2f}".format(METAStock.objects.first().close),
                'meta_change': "{:.2f}".format(METAStock.objects.last().close - METAStock.objects.first().close),
                'xom': "{:.2f}".format(XOMStock.objects.first().close),
                'xom_change': "{:.2f}".format(XOMStock.objects.last().close - XOMStock.objects.first().close),
                'pep': "{:.2f}".format(PEPStock.objects.first().close),
                'pep_change': "{:.2f}".format(PEPStock.objects.last().close - PEPStock.objects.first().close),
            }
            return render(request, "trade/trade.html", context=context)
    else:
        # Returns the user to the login/sign-up page if not logged in
        return redirect('/')
            
