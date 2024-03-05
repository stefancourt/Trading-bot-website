from django.urls import path

from .views import trade_view

urlpatterns = [
    path('', trade_view, name="trade")
]
