from django.shortcuts import render

def aitrade_view(request):
    return render(request, "aitrade/aitrade.html", context={})