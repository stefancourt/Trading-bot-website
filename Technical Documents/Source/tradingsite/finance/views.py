from django.shortcuts import render, redirect
from main.models import UserProfile
from finance.forms import ManageForm
from django.http import JsonResponse

def finance_view(request):
    if request.user.is_authenticated:
        # Obtains the user logged in
        user_profile = UserProfile.objects.get(user=request.user)
        user_total = user_profile.money_in_account
        if request.method == "POST":
            form = ManageForm(request.POST)
            if form.is_valid():
                # Process the form data
                rent = form.cleaned_data['rent']
                bills = form.cleaned_data['bills']
                food = form.cleaned_data['food']
                invest = form.cleaned_data['invest']
                savings = form.cleaned_data['savings']
                luxury = form.cleaned_data['luxury']
                choices = form.cleaned_data['choices']
            context={
                'manage_form': ManageForm(),
            }
            # If a post request is opened data is sent to the js console
            return JsonResponse({"choices":choices,
                                "rent":rent, 
                                "bills":bills, 
                                "food":food, 
                                "invest":invest,
                                "savings":savings,
                                "luxury":luxury,
                                "total":user_total})

        else:
            context={
                "user_total": "{:.2f}".format(user_total),
                'manage_form': ManageForm(),
            }
            return render(request, "finance/finance.html", context=context)
    else:
        # Returns the user to the login/sign-up page if not logged in
        return redirect('/')