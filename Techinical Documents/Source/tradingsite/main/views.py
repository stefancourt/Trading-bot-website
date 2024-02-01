from django.shortcuts import render

def stats_view(request):
    return render(request, "main/stats.html", context={})