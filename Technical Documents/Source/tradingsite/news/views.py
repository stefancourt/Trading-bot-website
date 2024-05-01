from django.shortcuts import render, redirect
from main.models import UserProfile
from trade.forms import TypeForm
from trade.models import AAPLStock, MSFTStock, JNJStock, JPMStock, PFEStock, BACStock
import json

def news_view(request):
    if request.user.is_authenticated:
        # Obtains the user logged in
        user = UserProfile.objects.get(user=request.user)
        user_total = user.money_in_account
        # Pre-processing for showing the latest stock price
        apple = AAPLStock.objects.all().order_by('-date')
        microsoft = MSFTStock.objects.all().order_by('-date')
        jnj = JNJStock.objects.all().order_by('-date')
        pfe = PFEStock.objects.all().order_by('-date')
        jpm = JPMStock.objects.all().order_by('-date')
        bac = BACStock.objects.all().order_by('-date')
        titles = []
        summaries = []
        relevance_scores = []
        if request.method == "POST":
            form = TypeForm(request.POST)
            if form.is_valid():
                stock_type = form.cleaned_data['stock_type']
                if stock_type == "Apple":
                    stock_type = "AAPL"
                elif stock_type == "Microsoft":
                    stock_type = "MSFT"
                elif stock_type == "Jhonson&Jhonson":
                    stock_type = "JNJ"
                elif stock_type == "Pfizer":
                    stock_type = "PFE"
                elif stock_type == "JPMorgan":
                    stock_type = "JPM"
                elif stock_type == "BankofAmerica":
                    stock_type = "BAC"
                # Allows choice of stock for news shown
                with open(f'stock_data/news/{stock_type}_news.json') as json_data:
                    data = json.load(json_data)
                    # Obtains the title and summary for the news of stock
                    for item in data['feed'][:10]:
                        titles.append(item['title'])
                        summaries.append(item['summary'])
                        # Gets all relevance scores for the news of stock
                        for i in item["ticker_sentiment"]:
                            if i['ticker'] == stock_type:
                                relevance_scores.append(i['relevance_score'])
                context = {
                    'money_in_account': "{:.2f}".format(user_total),
                    'stock_type_form': TypeForm(),
                    'summary_1':summaries[0],
                    'summary_2':summaries[1],
                    'summary_3':summaries[2],
                    'summary_4':summaries[3],
                    'summary_5':summaries[4],
                    'summary_6':summaries[5],
                    'score_1':relevance_scores[0],
                    'score_2':relevance_scores[1],
                    'score_3':relevance_scores[2],
                    'score_4':relevance_scores[3],
                    'score_5':relevance_scores[4],
                    'score_6':relevance_scores[5],
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
                }
                return render(request, "news/news.html", context=context)
        else:
            # Apple has been chose as the default news when the page is opened
            with open('stock_data/news/AAPL_news.json') as json_data:
                data = json.load(json_data)
                # Obtains the title and summary for the news of Apple stock
                for item in data['feed'][:10]:
                    titles.append(item['title'])
                    summaries.append(item['summary'])
                    for i in item["ticker_sentiment"]:
                        # Gets all relevance scores for the news of Apple stock
                        if i['ticker'] == 'AAPL':
                            relevance_scores.append(i['relevance_score'])
            context = {
                'money_in_account': "{:.2f}".format(user_total),
                'stock_type_form': TypeForm(),
                'summary_1':summaries[0],
                'summary_2':summaries[1],
                'summary_3':summaries[2],
                'summary_4':summaries[3],
                'summary_5':summaries[4],
                'summary_6':summaries[5],
                'score_1':relevance_scores[0],
                'score_2':relevance_scores[1],
                'score_3':relevance_scores[2],
                'score_4':relevance_scores[3],
                'score_5':relevance_scores[4],
                'score_6':relevance_scores[5],
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
            }
            return render(request, "news/news.html", context=context)
    else:
        # Returns the user to the login/sign-up page if not logged in
        return redirect('/')