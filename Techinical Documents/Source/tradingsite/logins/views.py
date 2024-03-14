from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, CustomAuthenticationForm
from main.models import UserProfile

def register_view(request):
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        UserProfile.objects.create(user=user_obj)
        return redirect('/')
    context = {"form": form}
    return render(request, 'logins/register.html', context)

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/stats')
    else:
        form = CustomAuthenticationForm(request)
    context = {
            "form": form
    }
    return render(request, 'logins/login.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    return render(request, 'logins/logout.html', {})