from django.shortcuts import render

def login_view(request):
    return render(request, "logins/login.html", context={})

def register_view(request):
    return render(request, "logins/register.html", context={})