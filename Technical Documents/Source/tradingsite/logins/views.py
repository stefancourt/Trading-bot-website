from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterUserForm, CustomAuthenticationForm
from main.models import UserProfile

def register_view(request):
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        # Saves the form
        user_obj = form.save()
        # Creates a user in UserProfile model
        UserProfile.objects.create(user=user_obj)
        return redirect('/')
    context = {"form": form}
    return render(request, 'logins/register.html', context)

def login_view(request):
    if request.method == "POST":
        # A CustomAuthenticationForm is used to allow different fields
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Logs in the user
            login(request, user)
            # Takes the user to the stats page (home page)
            return redirect('/stats')
    else:
        # Shows the CustomAuthenticationForm
        form = CustomAuthenticationForm(request)
    context = {
            "form": form
    }
    return render(request, 'logins/login.html', context)

def logout_view(request):
    if request.method == "POST":
        # Logs out the user
        logout(request)
        # Returns the user to login page
        return redirect("/")
    return render(request, 'logins/logout.html', {})